import axios, {  type AxiosProgressEvent, type AxiosRequestConfig } from 'axios';
import type{ IMapMarker } from '@/interfaces/IMapMarkers';

const VITE_API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
    baseURL: VITE_API_URL,
    withCredentials: true,
})

export default class Api {
    static async get(url: string, config?: AxiosRequestConfig) {
        return await api.get(url, config)
        .then(resp=>resp.data)
        .catch(e=>{
           console.error(e)
        })
    }

    static async post(url: string, data?: IMapMarker | FormData) {
      return api.post(url, data)
       .then(resp=> resp.data)
        .catch(e=>{
           console.error(e)
    })
}
    static async put(
        url: string,
        data?: FormData
    ) {
        return (await api.put(url, data))
    }

    static async delete(url: string, data?: number[]) {
        return await api.delete(url, { data })
    }
}