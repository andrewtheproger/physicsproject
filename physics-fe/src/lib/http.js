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
                method: 'GET',
                headers: {
                    'Authorization': 'Bearer ' + jwt
                }
            }).then(
                (response) => {
                    response.data = {
                        ...response.data,
                        isAdmin: response.data.role === 'admin'
                    };

                    return response;
                },
                error => {
                    if (!error.response || ![404, 403].includes(error.response.status)) {
                        throw error;
                    }
                    return Promise.resolve({
                        isAdmin: false,
                        is_token_expired: true,
                        role: null
                    })
                }
            )
        }
}
