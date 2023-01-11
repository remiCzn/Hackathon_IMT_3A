# Auth Web Microservice with rust using Actix-Web 4.0

##### Flow of the event would look like this:

- Registers with email address ➡ Receive an 📨 with a link to verify
- Follow the link ➡ register with same email and a password
- Login with email and password ➡ Get verified and receive auth cookie

##### Crates Used

-   [actix-web](https://crates.io/crates/actix-web) // Actix web is a simple, pragmatic and extremely fast web framework for Rust.
-   [chrono](https://crates.io/crates/chrono) // Date and time library for Rust.
-   [derive_more](https://crates.io/crates/derive_more) // Convenience macros to derive traits easily
-   [diesel](https://crates.io/crates/diesel) // A safe, extensible ORM and Query Builder for PostgreSQL, SQLite, and MySQL.
-   [dotenv](https://crates.io/crates/dotenv) // A dotenv implementation for Rust.
-   [env_logger](https://crates.io/crates/env_logger) // A logging implementation for log which is configured via an environment variable.
-   [futures](https://crates.io/crates/futures) // An implementation of futures and streams featuring zero allocations, composability, and iterator-like interfaces.
-   [lazy_static](https://docs.rs/lazy_static) // A macro for declaring lazily evaluated statics.
-   [r2d2](https://crates.io/crates/r2d2) // A generic connection pool.
-   [rust-argon](crates.io/crates/rust-argon2) // crate for hashing passwords using the cryptographically-secure Argon2 hashing algorithm.
-   [serde](https://crates.io/crates/serde) // A generic serialization/de-serialization framework.
-   [serde_json](https://crates.io/crates/serde_json) // A JSON serialization file format.
-   [sparkpost](https://crates.io/crates/sparkpost) // Rust bindings for sparkpost email api v1.
-   [uuid](https://crates.io/crates/uuid) // A library to generate and parse UUIDs.
-   [time](https://crates.io/crates/time) // Date and time library.
