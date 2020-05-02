import config from "../config/api.js";
import axios from "axios";
{
  axios;
}

export default {
  get_error_message(code) {
    switch (code) {
      case 1:
        return "разработчик сделал что-то не так";
      case 2:
        return "задачи с таким номером нет";
      case 3:
        return "задача с таким номером уже есть";
      case 4:
        return "подсказка не найдена";
      case 5:
        return "пользователя с такой почтой нет";
      case 6:
        return "пользователь с такой почтой уже есть";
      case 7:
        return "изображение не найдено";
      default:
        throw "This should not happens";
    }
  },
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
