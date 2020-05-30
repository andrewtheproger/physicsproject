export default {
  apiPrefix:
    "http://ec2-3-120-108-152.eu-central-1.compute.amazonaws.com:5000/api",
  // apiPrefix: "http://127.0.0.1:5000/api",
  defaultUser: {
    is_token_expired: true,
    role: null,
    color_background_primary: "#252525",
    color_background_secondary: "#555555",
    color_background_action: "#448aff",
    color_foreground_primary: "#cccccc",
    color_foreground_secondary: "#ccccff",
    color_foreground_action: "#ffffff",
    font_size: "20px"
  },
  datetime_format: {
    day: "2-digit",
    year: "numeric",
    month: "short",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit"
  }
};
