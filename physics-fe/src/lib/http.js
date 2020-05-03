import config from "../config/api.js";
import axios from "axios";
{
  axios;
}

export default {
  getMeAsUser(jwt) {
    const url = config.apiPrefix + "/users/me";

    return axios({
      url: url,
      method: "GET",
      headers: {
        Authorization: jwt
      }
    }).then(
      response => {
        if (response.data.email) {
          response.data = {
            ...response.data,
            isAdmin: response.data.role === "admin"
          };
        } else {
          response.data = {
            isAdmin: false,
            is_token_expired: true,
            role: null
          };
        }

        return response;
      },
      error => {
        console.log(error);
      }
    );
  }
};
