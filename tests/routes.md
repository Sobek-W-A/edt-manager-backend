# routes.md

base url localhost:8000/

| HTTP   | Route         | code | tested |
| ------ | ------------- | ---- | ------ |
| GET    | /account/     | 200  | yes    |
| GET    | /account/{id} | 200  | yes    |
| POST   | /account/     | 201  | yes    |
| PATCH  | /account/{id} | 205  | yes    |
| DELETE | /account/{id} | 204  | no     |
|        |               |      |        |
| POST   | /auth/login   | 200  | N/A    |
| POST   | /auth/logout  | 204  | N/A    |
| POST   | /auth/refresh | 200  | N/A    |
|        |               |      |        |
| GET    | /profile/     | 200  | yes    |
| GET    | /profile/{id} | 200  | yes    |
| GET    | /profile/me   | 200  | yes    |
| POST   | /profile/     | 201  | yes    |
| PATCH  | /profile/{id} | 205  | yes    |
| DELETE | /profile/{id} | 204  | no     |
