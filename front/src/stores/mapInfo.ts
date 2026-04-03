import { defineStore } from "pinia";

export const useMapInfoData = defineStore('mapInfoData', {
    state: () => ({
      points: []
    }),

    actions: {
        setPoints(points: []){
            this.points = points;
        }
    },

    getters: {
        getPoints: (state)=> state.points,
    }
});