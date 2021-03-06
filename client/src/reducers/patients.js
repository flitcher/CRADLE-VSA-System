// import all the actions here

import {
    GET_PATIENTS,
    GET_PATIENTS_REQUESTED,
    GET_PATIENTS_ERR,
    GET_PATIENT,
    GET_PATIENT_REQUESTED,
    GET_PATIENT_ERR
    // UPDATE_PATIENT,
    // UPDATE_PATIENT_REQUESTED,
    // UPDATE_PATIENT_ERR
} from '../actions/patients'
import { sortPatientsByLastReading } from '../containers/patientPage/patientUtils'

const initialState = {
    patient: {},
    patientsList: [],
    isLoading: true
}

export default (state = initialState, action) => {
    switch (action.type) {
        case GET_PATIENTS:
            const patientsList = action.payload.data
            patientsList.sort((a, b) => sortPatientsByLastReading(a, b))
            return {
                ...state,
                patientsList: patientsList,
                isLoading: false
            }

        case GET_PATIENTS_REQUESTED:
            return {
                ...state,
                isLoading: true
            }

        case GET_PATIENTS_ERR:
            return {
                ...state,
                isLoading: false
            }
        case GET_PATIENT:
            return {
                ...state,
                patient: action.payload.data,
                isLoading: false
            }

        case GET_PATIENT_REQUESTED:
            return {
                ...state,
                isLoading: true
            }

        case GET_PATIENT_ERR:
            return {
                ...state,
                isLoading: false
            }

        default:
            return state
    }
}
