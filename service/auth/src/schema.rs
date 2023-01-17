// @generated automatically by Diesel CLI.

diesel::table! {
    invitations (id) {
        id -> Varchar,
        email -> Varchar,
        expires_at -> Timestamp,
    }
}

diesel::table! {
    users (email) {
        email -> Varchar,
        hash -> Varchar,
        created_at -> Timestamp,
    }
}

diesel::allow_tables_to_appear_in_same_query!(
    invitations,
    users,
);
