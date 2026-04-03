import { defineStore } from "pinia";
import type { IMapMarker } from "@/interfaces/IMapMarkers";
export const useMapInfoData = defineStore('mapInfoData', {
    state: () => ({
      points: [] as IMapMarker[]
    }),

    actions: {
        setPoints(points: IMapMarker[]){
            this.points = points;
        }
    },

    getters: {
        getPoints: (state)=> state.points,
    }
});