import router from "@/router/index";

const API_URL = "http://localhost:5000";
const LOGIN_URL = API_URL + "/login";
const SIGNUP_URL = API_URL + "/signup";

export default {
  user: {
    authenticated: false,
    usertype:1
  },

  login(context, creds, redirect) {
    context.$http.post(LOGIN_URL, creds).then(
      data => {
        localStorage.setItem("access_token", data.acces_token);
        localStorage.setItem("refresh_token", data.refresh_token);

        this.user.authenticated = true;

        if (redirect) {
          router.go(redirect);
        }
      },
      error => {
        context.error = error.message;
      }
    );
  },

  signup(context, creds, redirect) {
    context.$http.post(SIGNUP_URL, creds).then(
      response => {
        localStorage.setItem("access_token", response.access_token);
        localStorage.setItem("refresh_token", response.refresh_token);
        this.user.authenticated = true;

        if (redirect) {
          router.go(redirect);
        }
      },
      error => {
        context.error = error.message;
      }
    );
  },

  logout() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    this.user.authenticated = false;
    router.go("/");
  },

  checkAuth() {
    var jwt = localStorage.getItem("access_token");
    var usertype = localStorage.getItem('user_type')
    if (jwt) {
      this.user.authenticated = true;
    } else {
      this.user.authenticated = false;
    }
    if(usertype){
      this.user.usertype = Number(usertype)
    }
    console.log(this.user.authenticated)
  },

  getAuthHeader() {
    return {
      Authorization: "Bearer " + localStorage.getItem("access_token")
    };
  }
};
