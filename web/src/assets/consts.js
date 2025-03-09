export const API_BASE_URL = process.env.REACT_APP_API_URL;

export const API_AUTH_LOGIN_URL = API_BASE_URL + "/auth/login";
export const API_AUTH_REGISTER_URL = API_BASE_URL + "/auth/register";
export const API_AUTH_CHECK_URL = API_BASE_URL + "/auth/check";

export const API_ACCOUNT_ARTICLES = API_BASE_URL + "/account/articles";
export const API_ACCOUNT_ARTICLES_GENERATE = API_BASE_URL + "/account/articles/{{id}}/generate";

export const API_ACCOUNT_POSTS = API_BASE_URL + "/account/posts";

export const API_ACCOUNT_SETTINGS = API_BASE_URL + "/account/settings";
