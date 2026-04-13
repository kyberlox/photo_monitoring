import type { LngLat } from '@yandex/ymaps3-types';

export interface IMapMarker{
    id?: number,
    name?: string,
    coordinates?: LngLat | [],
    photos?:IPhoto[]
}

export interface IPhoto{
    title: string,
    comment: null | string,
    id: number,
    created_at: string,
    file_url: string,
    location_id: number
}