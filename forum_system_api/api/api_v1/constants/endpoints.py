API_BASE_PATH = '/api/v1'

USERS_ENDPOINT = API_BASE_PATH + '/users'

USERS_ME_ENDPOINT = USERS_ENDPOINT + '/me'
USERS_REGISTER_ENDPOINT = USERS_ENDPOINT + '/register'
USERS_PERMISSIONS_LIST_ENDPOINT = USERS_ENDPOINT + '/permissions/{}'
USERS_PERMISSIONS_DETAIL_ENDPOINT = USERS_ENDPOINT + '/{}/permissions'
USERS_GRANT_READ_PERMISSION_ENDPOINT = USERS_ENDPOINT + '/{}/permissions/{}/read-permission'
USERS_GRANT_WRITE_PERMISSION_ENDPOINT = USERS_ENDPOINT + '/{}/permissions/{}/write-permission'
USERS_REVOKE_PERMISSION_ENDPOINT = USERS_ENDPOINT + '/{}/permissions/{}'

CATEGORY_ENDPOINT_CREATE_CATEGORY = "/api/v1/categories/"
CATEGORY_ENDPOINT_GET_CATEGORIES = "/api/v1/categories/"
CATEGORY_ENDPOINT_VIEW_CATEGORY = "/api/v1/categories/{}/topics/"
CATEGORY_PRIVACY_ENDPOINT = "/api/v1/categories/{}/private/"
CATEGORY_LOCK_ENDPOINT = "/api/v1/categories/{}/lock/"