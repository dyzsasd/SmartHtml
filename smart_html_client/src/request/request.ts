import axios, { AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  timeout: 30000,
  headers: {'Content-Type': 'application/json;charset=utf-8'}
});

axiosInstance.interceptors.request.use(config => {
  // config.headers['Authorization'] = 'Bearer '+ localStorage.getItem("access_token");
  config.headers['Content-Type'] = 'application/json;charset=utf-8';
  return config
}, error => {
  return Promise.reject(error)
});

axiosInstance.interceptors.response.use( 
  (response: AxiosResponse) =>  Promise.resolve(response),
  (error: AxiosError) => Promise.reject(error),
)

const Get = async <T = unknown>(
  url: string,
  config?: AxiosRequestConfig,
): Promise<T> => {
  try {
    const response = await axiosInstance.get<T>(url, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

const Post = async <T = unknown>(
  url: string,
  data?: unknown,
  config?: AxiosRequestConfig,
): Promise<T> => {
  try {
    const response = await axiosInstance.post<T>(url, data, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

const Delete = async <T = unknown>(
  url: string,
  config?: AxiosRequestConfig,
): Promise<T> => {
  try {
    const response = await axiosInstance.delete<T>(url, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};


const Put = async <T = unknown>(
  url: string,
  data?: unknown,
  config?: AxiosRequestConfig,
): Promise<T> => {
  try {
    const response = await axiosInstance.put<T>(url, data, config);
    return response.data;
  } catch (error) {
    throw error;
  }
};

export default {
  get: Get,
  post: Post,
  put: Put,
  delete: Delete
}
