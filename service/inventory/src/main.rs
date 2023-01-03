use actix_web::{get, post, put, delete, web, App, HttpRequest, HttpResponse, HttpServer, Responder, ResponseError};
use actix_web::http::header::ContentType;
use actix_web::http::StatusCode;
use actix_web::body::BoxBody;

use serde::{Serialize, Deserialize};

use std::fmt::Display;
use std::sync::Mutex;

static PATH: &str = "data/inventories.json";


#[derive(Debug, Serialize, Deserialize)]
struct UserInventory
{
    user_id: String,
    game_inventories: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct GameInventory
{
    id: String,
    game_id: String,
    items: Vec<(String, u32)>,
}

impl PartialEq for GameInventory {
    fn eq(&self, other: &Self) -> bool {
        self.id == other.id
    }
}

#[derive(Debug, Serialize, Deserialize)]
struct Item
{
    id: String,
    name: String,
    game_id: String,
}

impl Responder for UserInventory {
    type Body = BoxBody;

    fn respond_to(self, _req: &HttpRequest) -> HttpResponse<Self::Body> {
        let res_body = serde_json::to_string(&self).unwrap();
        HttpResponse::Ok()
        .content_type(ContentType::json())
        .body(res_body)
    }
}

impl Responder for GameInventory {
    type Body = BoxBody;

    fn respond_to(self, _req: &HttpRequest) -> HttpResponse<Self::Body> {
        let res_body = serde_json::to_string(&self).unwrap();
        HttpResponse::Ok()
        .content_type(ContentType::json())
        .body(res_body)
    }
}

impl Responder for Item {
    type Body = BoxBody;

    fn respond_to(self, _req: &HttpRequest) -> HttpResponse<Self::Body> {
        let res_body = serde_json::to_string(&self).unwrap();
        HttpResponse::Ok()
        .content_type(ContentType::json())
        .body(res_body)
    }
}

#[derive(Debug, Serialize)]
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
    user_inventories: Mutex<Vec<UserInventory>>,
    game_inventories: Mutex<Vec<GameInventory>>,
    items: Mutex<Vec<Item>>,

}

#[post("/inventories")]
async fn create_user_inventory(user_inventory: web::Json<UserInventory>, data: web::Data<DataState>) -> impl Responder {
    let new_user_inventory: UserInventory = user_inventory.0;
    let mut user_inventories = data.user_inventories.lock().unwrap();
    let response = serde_json::to_string(&new_user_inventory).unwrap();
    user_inventories.push(new_user_inventory);

    HttpResponse::Created()
    .content_type(ContentType::json())
    .body(response)
}

#[get("/inventories")]
async fn get_inventories(data: web::Data<DataState>) -> impl Responder {
    let user_inventories = data.user_inventories.lock().unwrap();

    let response = serde_json::to_string(&(*user_inventories)).unwrap();

   HttpResponse::Ok()
       .content_type(ContentType::json())
   .body(response)
}

#[get("/inventories/{user_id}")]
async fn get_user_inventory(user_id: web::Path<String>, data: web::Data<DataState>) -> Result<UserInventory, ErrNoId> {
    let user_id: String = String::from(&*user_id);
    let user_inventories = data.user_inventories.lock().unwrap();

    let user_inventory: Vec<_> = user_inventories.iter()
    .filter(|x| x.user_id == user_id)
    .collect();
    if !user_inventory.is_empty() {
        Ok(UserInventory {
            user_id: String::from(&user_inventory[0].user_id),
            game_inventories: user_inventory[0].game_inventories.iter().map(|x| String::from(x)).collect()
        })
    } else {
        let response = ErrNoId {
            id: user_id,
            err: String::from("user inventory not found")
        };
        Err(response)
    }
}

#[delete("/inventories/{user_id}")]
async fn delete_user_inventory(user_id: web::Path<String>, data: web::Data<DataState>) -> Result<UserInventory, ErrNoId> {
    let user_id: String = String::from(&*user_id);
    let mut user_inventories = data.user_inventories.lock().unwrap();

    let index = user_inventories.iter()
    .position(|x| x.user_id == user_id);

    match index {
        Some(id) => {
            let deleted_user_inventory = user_inventories.remove(id);
            Ok(deleted_user_inventory)
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

#[post("/inventories/{user_id}")]
async fn create_user_game_inventory(user_id: web::Path<String>, user_game_inventory: web::Json<GameInventory>, data: web::Data<DataState>) -> Result<UserInventory, ErrNoId> {
    let user_id: String = String::from(&*user_id);
    let new_user_game_inventory: GameInventory = user_game_inventory.0;
    let mut user_inventories = data.user_inventories.lock().unwrap();
    let mut game_inventories = data.game_inventories.lock().unwrap();


    let index = user_inventories.iter()
    .position(|x| x.user_id == user_id);


    match index {
        Some(id) => {
            user_inventories[id].game_inventories.push(String::from(&new_user_game_inventory.id));
            game_inventories.push(new_user_game_inventory);

            Ok(UserInventory {
                user_id: String::from(&user_inventories[id].user_id),
                game_inventories: user_inventories[id].game_inventories.iter().map(|x| String::from(x)).collect()
            })
        },
        None => {
            let response = ErrNoId {
                id: user_id,
                err: String::from("user inventory not found")
            };
            Err(response)
        }
    }
}

#[delete("/inventories/{user_id}/{game_id}")]
async fn delete_user_game_inventory(user_id: web::Path<String>, game_id: web::Path<String>, data: web::Data<DataState>) -> Result<GameInventory, ErrNoId> {
    let user_id: String = String::from(&*user_id);
    let game_id: String = String::from(&*game_id);
    let mut user_inventories = data.user_inventories.lock().unwrap();

    let index = user_inventories.iter()
    .position(|x| x.user_id == user_id);

    match index {
        Some(user_id) => {
            let mut game_inventories = data.game_inventories.lock().unwrap();

            let index = game_inventories.iter()
            .position(|x| x.game_id == game_id);

            match index {
                Some(game_inventory_id) => {
                    let user_game_id = user_inventories[user_id].game_inventories.iter().position(|x| x == &game_inventories[game_inventory_id].id);
                    user_inventories[user_id].game_inventories.remove(user_game_id.unwrap());

                    let deleted_user_game_inventory = game_inventories.remove(game_inventory_id);
                    Ok(deleted_user_game_inventory)
                },
                None => {
                    let response = ErrNoId {
                        id: game_id,
                        err: String::from("game not found")
                    };
                    Err(response)
                }
            }
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

#[post("/items")]
async fn create_item(item: web::Json<Item>, data: web::Data<DataState>) -> impl Responder {
    let new_item: Item = item.0;
    let mut items = data.items.lock().unwrap();
    let response = serde_json::to_string(&new_item).unwrap();
    items.push(new_item);

    HttpResponse::Created()
    .content_type(ContentType::json())
    .body(response)
}

#[get("/items/{user_id}/{item_id}/{amount}")]
async fn add_user_item(user_id: web::Path<String>, item_id: web::Path<String>, amount: web::Path<u32>, data: web::Data<DataState>) -> Result<UserInventory, ErrNoId> {
    let user_id: String = String::from(&*user_id);
    let item_id: String = String::from(&*item_id);
    let amount: u32 = amount.into_inner();

    let user_inventories = data.user_inventories.lock().unwrap();

    let id = user_inventories.iter().position(|x| x.user_id == user_id);

    match id {
        Some(_) => {
            let items = data.items.lock().unwrap();

            let id = items.iter().position(|x| x.id == item_id);

            match id {
                Some(item_index) => {
                    let item = &items[item_index];

                    let mut game_inventories = data.game_inventories.lock().unwrap();

                    let id = game_inventories.iter().position(|x| &x.game_id == &item.game_id);

                    match id {
                        Some(game_index) => {
                            let id = game_inventories[game_index].items.iter().position(|(item, _)| item == &item_id);

                            match id {
                                Some(item_inv_index) => {
                                    let (item_id, old_amount) = game_inventories[game_index].items.remove(item_inv_index);
                                    game_inventories[game_index].items.push((item_id, old_amount + amount));
                                },
                                None => {
                                    game_inventories[game_index].items.push((item_id, amount));
                                }
                            }

                            Ok(UserInventory {
                                user_id: String::from(&user_inventories[item_index].user_id),
                                game_inventories: user_inventories[item_index].game_inventories.iter().map(|x| String::from(x)).collect()
                            })
                        },
                        None => {
                            let response = ErrNoId {
                                id: String::from(&item.game_id),
                                err: String::from("the user has no game inventory for this game id")
                            };
                            Err(response)
                        }
                    }
                },
                None => {
                    let response = ErrNoId {
                        id: item_id,
                        err: String::from("item not found")
                    };
                    Err(response)
                }
            }
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
    let data_state = web::Data::new(DataState {
        user_inventories: Mutex::new(vec![
        UserInventory {
            user_id: String::from("5c62e335-abfa-407f-81c6-590fb6bc2b70"),
            game_inventories: vec![String::from("a5023011-ca5e-445c-b2b1-49a8dd40cddc"), String::from("3e478cb2-ef56-4e77-9fc2-60508dd11030")]

        },
        UserInventory {
            user_id: String::from("4919b8dd-a6c3-4f5b-9739-c7060d8847dc"),
            game_inventories: vec![]
        }
        ]),
        game_inventories: Mutex::new(vec![
        GameInventory {
            id: String::from("a5023011-ca5e-445c-b2b1-49a8dd40cddc"),
            game_id: String::from("33445d6e-15a8-4dbf-8e71-170b2e02c06d"),
            items: vec![(String::from("e8fc1bd3-7666-42e6-872a-82490135502c"), 14), (String::from("d12edc41-ab7c-4784-b420-668c10ef2f95"), 8)]
        },
        GameInventory {
            id: String::from("3e478cb2-ef56-4e77-9fc2-60508dd11030"),
            game_id: String::from("a8d4ef67-23f8-4833-af5c-75b4398de229"),
            items: vec![]
        }
        ]),
        items: Mutex::new(vec![
        Item {
            id: String::from("510d2070-1499-4d07-b5af-0697213e58f8"),
            name: String::from("Ultra ball"),
            game_id: String::from("33445d6e-15a8-4dbf-8e71-170b2e02c06d")
        },
        Item {
            id: String::from("e8fc1bd3-7666-42e6-872a-82490135502c"),
            name: String::from("Super ball"),
            game_id: String::from("33445d6e-15a8-4dbf-8e71-170b2e02c06d")
        },
        Item {
            id: String::from("d12edc41-ab7c-4784-b420-668c10ef2f95"),
            name: String::from("Super potion"),
            game_id: String::from("33445d6e-15a8-4dbf-8e71-170b2e02c06d")
        }
        ])
    });

    HttpServer::new(move || {
        App::new()
        .app_data(data_state.clone())
        .service(create_user_inventory)
        .service(get_user_inventory)
        .service(get_inventories)
        .service(create_user_game_inventory)
        .service(create_item)
        .service(delete_user_inventory)
        .service(delete_user_game_inventory)
        .service(add_user_item)
    })
    .bind(("127.0.0.1", 3010))?
    .run()
    .await
}
