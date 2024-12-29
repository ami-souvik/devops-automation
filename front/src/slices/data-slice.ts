import { createSlice } from '@reduxjs/toolkit'

export const dataSlice = createSlice({
  name: 'data',
  initialState: {
    appname: "",
    az: "ap-south-1",
  },
  reducers: {
    setApp: (state, action) => {
      const { appname, az } = action.payload
      state.appname = appname
      state.az = az
    },
    setAppname: (state, action) => {
      state.appname = action.payload
    },
    setAz: (state, action) => {
      state.az = action.payload
    }
  },
})

// Action creators are generated for each case reducer function
export const { setApp, setAppname, setAz } = dataSlice.actions

export default dataSlice.reducer