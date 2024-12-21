# routes.md

base url localhost:8000/

| HTTP   | Route         | code |
| ------ | ------------- | ---- |
| GET    | /account/     | 200  |
| GET    | /account/{id} | 200  |
| POST   | /account/     | 201  |
| PATCH  | /account/{id} | 205  |
| DELETE | /account/{id} | 204  |
|        |               |      |
| POST   | /auth/login   | 200  |
| POST   | /auth/logout  | 204  |
| POST   | /auth/refresh | 200  |
|        |               |      |
| GET    | /profile/     | 200  |
| GET    | /profile/{id} | 200  |
| GET    | /profile/me   | 200  |
| POST   | /profile/     | 201  |
| PATCH  | /profile/{id} | 205  |
| DELETE | /profile/{id} | 204  |
