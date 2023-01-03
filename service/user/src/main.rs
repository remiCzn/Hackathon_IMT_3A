use actix_web::{get, post, put, delete, web, App, HttpRequest, HttpResponse, HttpServer, Responder, ResponseError};
use actix_web::http::header::ContentType;
use actix_web::http::StatusCode;
use actix_web::body::BoxBody;

use serde::{Serialize, Deserialize};

use std::fmt::Display;
use std::sync::Mutex;

use utoipa::{ToSchema};

use utoipa::{
    openapi::security::{ApiKey, ApiKeyValue, SecurityScheme},
    Modify, OpenApi,
};

static PATH: &str = "data/users.json";


#[derive(Debug, Serialize, Deserialize, ToSchema)]
struct User {
    id: String,
    name: String,
    password: String,
    inventory_id: String,
    administrator: bool,
}

impl Responder for User {
    type Body = BoxBody;

    fn respond_to(self, _req: &HttpRequest) -> HttpResponse<Self::Body> {
        let res_body = serde_json::to_string(&self).unwrap();
        HttpResponse::Ok()
        .content_type(ContentType::json())
        .body(res_body)
    }
}

#[derive(Debug, Serialize, ToSchema)]
struct ErrNoId {
    id: String,
    err: String,
}

impl ResponseError for ErrNoId {
    fn status_code(&self) -> StatusCode {
        StatusCode::NOT_FOUND
    }

    fn error_response(&self) -> HttpResponse<BoxBody> {
        let body = serde_json::to_string(&self).unwrap();
        let res = HttpResponse::new(self.status_code());
        res.set_body(BoxBody::new(body))
    }
}

impl Display for ErrNoId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{:?}", self)
    }
}

struct DataState {
    users: Mutex<Vec<User>>,
}

#[utoipa::path(
        request_body = User,
        responses(
                (status = 201, description = "User created successfully", body = User),
                (status = 409, description = "User with id already exists", body = ResponseError)
        )
)]
#[post("/users")]
async fn create_user(user: web::Json<User>, data: web::Data<DataState>) -> impl Responder {
    let new_user: User = user.0;
    let mut users = data.users.lock().unwrap();
    let response = serde_json::to_string(&new_user).unwrap();
    users.push(new_user);

    HttpResponse::Created()
    .content_type(ContentType::json())
    .body(response)
}

#[utoipa::path(
        responses(
                (status = 200, description = "List current Users", body = [User])
        )
)]
#[get("/users")]
async fn get_users(data: web::Data<DataState>) -> impl Responder {
    let users = data.users.lock().unwrap();

   let response = serde_json::to_string(&(*users)).unwrap();

   HttpResponse::Ok()
       .content_type(ContentType::json())
   .body(response)
}

#[utoipa::path(
        responses(
                (status = 200, description = "User found from storage", body = User),
                (status = 404, description = "User not found by id", body = ErrNoId)
        ),
params(
        ("id", description = "Unique storage id of User")
)
)]
#[get("/users/{id}")]
async fn get_user(id: web::Path<String>, data: web::Data<DataState>) -> Result<User, ErrNoId> {
    let user_id: String = String::from(&*id);
    let users = data.users.lock().unwrap();

    let user: Vec<_> = users.iter()
    .filter(|x| x.id == user_id)
    .collect();
    if !user.is_empty() {
        Ok(User {
            id: String::from(&user[0].id),
            name: String::from(&user[0].name),
            password: String::from(&user[0].password),
            inventory_id: String::from(&user[0].inventory_id),
            administrator: user[0].administrator
        })
    } else {
        let response = ErrNoId {
            id: user_id,
            err: String::from("user not found")
        };
        Err(response)
    }
}

#[utoipa::path(
        responses(
                (status = 200, description = "User modified successfully"),
                (status = 401, description = "Unauthorized to modify User", body = ErrorResponse),
                (status = 404, description = "User not found by id", body = ErrNoId)
        ),
params(
        ("id", description = "Unique storage id of User")
),
security(
        ("api_key" = [])
)
)]
#[put("/users/{id}")]
async fn update_user(id: web::Path<String>, user: web::Json<User>, data: web::Data<DataState>) -> Result<HttpResponse, ErrNoId> {
    let user_id: String = String::from(&*id);

    let new_user: User = user.0;


    let mut users = data.users.lock().unwrap();

    let id_index = users.iter()
    .position(|x| x.id == user_id);

    match id_index {
        Some(id) => {
            let response = serde_json::to_string(&new_user).unwrap();
            users[id] = new_user;
            Ok(HttpResponse::Ok()
            .content_type(ContentType::json())
            .body(response)
            )
        },
        None => {
            let response = ErrNoId {
                id: user_id,
                err: String::from("user not found")
            };
            Err(response)
        }
    }
}

#[utoipa::path(
        responses(
                (status = 200, description = "User deleted successfully"),
                (status = 401, description = "Unauthorized to delete User", body = ErrorResponse),
                (status = 404, description = "User not found by id", body = ErrNoId)
        ),
params(
        ("id", description = "Unique storage id of User")
),
security(
        ("api_key" = [])
)
)]
#[delete("/users/{id}")]
async fn delete_user(id: web::Path<String>, data: web::Data<DataState>) -> Result<User, ErrNoId> {
    let user_id: String = String::from(&*id);
    let mut users = data.users.lock().unwrap();

    let id_index = users.iter()
    .position(|x| x.id == user_id);

    match id_index {
        Some(id) => {
            let deleted_user = users.remove(id);
            Ok(deleted_user)
        },
        None => {
            let response = ErrNoId {
                id: user_id,
                err: String::from("user not found")
            };
            Err(response)
        }
    }
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let users_state = web::Data::new(DataState {
        users: Mutex::new(vec![
        User {
            id: String::from("4919b8dd-a6c3-4f5b-9739-c7060d8847dc"),
            name: String::from("Jane Doe"),
            password: String::from("1234"),
            inventory_id: String::from("15ca4531-3626-43b8-8eab-21df4d34b318"),
            administrator: true
        },
        User {
            id: String::from("5c62e335-abfa-407f-81c6-590fb6bc2b70"),
            name: String::from("test"),
            password: String::from("1234"),
            inventory_id: String::from("45462b51-cf05-45f6-ae44-eaecdae38c29"),
            administrator: false
        }
        ])
    });

    #[derive(OpenApi)]
    #[openapi(
            paths(get_users,
            create_user,
            delete_user,
            get_user,
            update_user
            ),
    components(
            schemas(User, ErrNoId)
    ),
    tags(
            (name = "users", description = "User management endpoints.")
    )
    )]
    struct ApiDoc;

    println!("{}", ApiDoc::openapi().to_pretty_json().unwrap());

    HttpServer::new(move || {
        App::new()
        .app_data(users_state.clone())
        .service(create_user)
        .service(get_users)
        .service(get_user)
        .service(update_user)
        .service(delete_user)
        .service(
                SwaggerUi::new("/swagger-ui/{_:.*}")
                .url("/api-doc/openapi.json", ApiDoc::openapi()),
        )
    })
    .bind(("127.0.0.1", 8600))?
    .run()
    .await
}
