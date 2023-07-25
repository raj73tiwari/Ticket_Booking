// // import axios from "axios";
// // import { useToast } from 'vue-toastification';
// // import { useUserStore } from './stores/users';



// // axios.defaults.baseURL = 'http://localhost:5000/'



// // axios.interceptors.request.use(req => {
// //   const accessToken = localStorage.getItem("token");
// //   if (req.url === "/refresh" && req.method === "post") {
// //     const refreshToken = localStorage.getItem("refresh_token");
// //     req.headers["Authorization"] = `Bearer ${refreshToken}`
// //   }
// //   else if (accessToken) {
// //     req.headers["Authorization"] = `Bearer ${accessToken}`
// //   }


// //   return req;
// // });






// // let refresh = false

// // // axios.interceptors.response.use((response) => response, async (e) => {

// // //   if (e.response.status === 401 && !refresh) {
// // //     refresh = true
// // //     const { status, data } = await axios.post('/refresh')

// // //     if (status === 200) {
// // //       console.log(data)
// // //       localStorage.setItem("token", data.access_token)
// // //       return axios(error.config)
// // //     }
// // //   }
// // //   refresh = false
// // //   return e
// // // });







// // // Define a variable to track the token refresh state
// // let isRefreshing = false;

// // // Define a variable to store the failed requests and their callbacks
// // const failedRequestsQueue = [];

// // // Add a response interceptor to handle successful responses
// // axios.interceptors.response.use(
// //   (response) => response,
// //   (error) => {
// //     const originalRequest = error.config;

// //     if (error.response && error.response.status === 401) {
// //       // Check if token is already being refreshed
// //       if (!isRefreshing) {
// //         isRefreshing = true;

// //         // Perform the token refresh request
// //         return axios.post('/refresh')
// //           .then((response) => {
// //             const newToken = response.data.access_token;
// //             localStorage.setItem('token', newToken);

// //             // Retry the original request with the new token
// //             originalRequest.headers['Authorization'] = `Bearer ${newToken}`;

// //             // Retry the failed request queue
// //             failedRequestsQueue.forEach((request) => request.resolve(newToken));
// //             failedRequestsQueue.length = 0; // Clear the queue

// //             return axios(originalRequest);
// //           })
// //           .catch((error) => {
// //             // If token refresh fails, log out the user or handle the error as needed
// //             const toast = useToast();
// //             const userStore=useUserStore();
// //             toast.warning('Please Login !')
// //             localStorage.removeItem("token");
// //             localStorage.removeItem("refresh_token");
// //             userStore.removeUser()

// //             // For example: logoutUser()
// //             return Promise.reject(error);
// //           })
// //           .finally(() => {
// //             isRefreshing = false;
// //           });
// //       } else {
// //         // If token is already being refreshed, add the request to the queue
// //         return new Promise((resolve, reject) => {
// //           failedRequestsQueue.push({ resolve, reject });
// //         })
// //           .then((newToken) => {
// //             originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
// //             return axios(originalRequest);
// //           })
// //           .catch((error) => {
// //             return Promise.reject(error);
// //           });
// //       }
// //     }
// //     return Promise.reject(error);
// //   }
// // );


// import axios from "axios";
// import { useToast } from 'vue-toastification';
// import { useUserStore } from './stores/users';

// axios.defaults.baseURL = 'http://localhost:5000/';

// axios.interceptors.request.use(req => {
//   const accessToken = localStorage.getItem("token");
//   if (req.url === "/refresh" && req.method === "post") {
//     const refreshToken = localStorage.getItem("refresh_token");
//     req.headers["Authorization"] = `Bearer ${refreshToken}`;
//   } else if (accessToken) {
//     req.headers["Authorization"] = `Bearer ${accessToken}`;
//   }
//   return req;
// });

// let isRefreshing = false;
// const failedRequestsQueue = [];

// axios.interceptors.response.use(
//   (response) => response,
//   async (error) => {
//     const originalRequest = error.config;

//     if (error.response && error.response.status === 401) {
//       if (!isRefreshing) {
//         isRefreshing = true;

//         try {
//           const response = await axios.post('/refresh');
//           const newToken = response.data.access_token;
//           localStorage.setItem('token', newToken);
//           originalRequest.headers['Authorization'] = `Bearer ${newToken}`;

//           failedRequestsQueue.forEach((request) => request.resolve(newToken));
//           failedRequestsQueue.length = 0;

//           return axios(originalRequest);
//         } catch (error) {
//           const toast = useToast();
//           const userStore = useUserStore();
//           toast.warning('Please Login !');
//           localStorage.removeItem("token");
//           localStorage.removeItem("refresh_token");
//           userStore.removeUser();

//           return Promise.reject(error);
//         } finally {
//           isRefreshing = false;
//         }
//       } else {
//         return new Promise((resolve, reject) => {
//           failedRequestsQueue.push({ resolve, reject });
//         })
//           .then((newToken) => {
//             originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
//             return axios(originalRequest);
//           })
//           .catch((error) => {
//             return Promise.reject(error);
//           });
//       }
//     }
//     return Promise.reject(error);
//   }
// );































import axios from "axios";

axios.defaults.baseURL = 'http://localhost:5000/';

axios.interceptors.request.use(req => {
  const accessToken = localStorage.getItem("token");
  if (req.url === "/refresh" && req.method === "post") {
    const refreshToken = localStorage.getItem("refresh_token");
    req.headers["Authorization"] = `Bearer ${refreshToken}`;
  } else if (accessToken) {
    req.headers["Authorization"] = `Bearer ${accessToken}`;
  }
  return req;
});

let isRefreshing = false;
const failedRequestsQueue = [];

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response && error.response.status === 401) {
      if (!isRefreshing) {
        isRefreshing = true;

        try {
          const response = await axios.post('/refresh');
          const newToken = response.data.access_token;
          localStorage.setItem('token', newToken);
          originalRequest.headers['Authorization'] = `Bearer ${newToken}`;

          failedRequestsQueue.forEach((request) => request.resolve(newToken));
          failedRequestsQueue.length = 0;

          return axios(originalRequest);
        } catch (error) {
          // Emit a custom event to handle token refresh failure in Vue component
          const event = new CustomEvent("token-refresh-failed");
          document.dispatchEvent(event);

          return Promise.reject(error);
        } finally {
          isRefreshing = false;
        }
      } else {
        return new Promise((resolve, reject) => {
          failedRequestsQueue.push({ resolve, reject });
        })
          .then((newToken) => {
            originalRequest.headers['Authorization'] = `Bearer ${newToken}`;
            return axios(originalRequest);
          })
          .catch((error) => {
            return Promise.reject(error);
          });
      }
    }
    return Promise.reject(error);
  }
);













