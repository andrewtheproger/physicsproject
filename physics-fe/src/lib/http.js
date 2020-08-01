import config from "../config/api.js";
const axios = () => import(/* webpackChunkName: "axios" */ "axios");

export default {
  predicate_numbers() {
    const url = config.apiPrefix + "/tasks/predicate_numbers";

    return axios().then(ax =>
      ax
        .request({
          url: url,
          method: "GET"
        }).then(
        result => {
          return result.data;
        },
        error => {
          throw error;
        }
      ));
  },
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
      case 8:
        return "неверный пароль";
      case 9:
        return "недостаточно прав. Проверьте, что вы залогинены";
      default:
        throw `This should not happens ${code}`;
    }
  },
  getMeAsUser(jwt) {
    const url = config.apiPrefix + "/users/me";

    return axios().then(ax =>
      ax
        .request({
          url: url,
          method: "GET",
          headers: {
            Authorization: jwt
          }
        })
        .then(
          response => {
            let user = response.data;

            if (!user.email) {
              user = config.defaultUser;
            }

            user.color_background_primary =
              user.color_background_primary ||
              config.defaultUser.color_background_primary;
            user.color_background_secondary =
              user.color_background_secondary ||
              config.defaultUser.color_background_secondary;
            user.color_background_action =
              user.color_background_action ||
              config.defaultUser.color_background_action;
            user.color_foreground_primary =
              user.color_foreground_primary ||
              config.defaultUser.color_foreground_primary;
            user.color_foreground_secondary =
              user.color_foreground_secondary ||
              config.defaultUser.color_foreground_secondary;
            user.color_foreground_action =
              user.color_foreground_action ||
              config.defaultUser.color_foreground_action;
            user.color_background_success =
              user.color_background_success ||
              config.defaultUser.color_background_success;
            user.color_background_warning =
              user.color_background_warning ||
              config.defaultUser.color_background_warning;
            user.color_background_error =
              user.color_background_error ||
              config.defaultUser.color_background_error;
            user.color_foreground_success =
              user.color_foreground_success ||
              config.defaultUser.color_foreground_success;
            user.color_foreground_warning =
              user.color_foreground_warning ||
              config.defaultUser.color_foreground_warning;
            user.color_foreground_error =
              user.color_foreground_error ||
              config.defaultUser.color_foreground_error;

            return {
              ...user,
              isAdmin: response.data.role === "admin"
            };
          },
          error => {
            throw error;
          }
        )
    );
  }
};
