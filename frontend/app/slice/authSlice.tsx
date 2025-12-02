import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const performLogout = createAsyncThunk('auth/performLogout', async (_, thunkAPI) => {
  try {
    const res = await fetch('/auth/logout', {
      method: 'POST',
      credentials: 'include', 
      headers: { 'Accept': 'application/json' },
    });
    if (!res.ok) {
      const text = await res.text();
      return thunkAPI.rejectWithValue(text);
    }
    const data = await res.json().catch(() => ({}));
    return data;
  } catch (err) {
    return thunkAPI.rejectWithValue(String(err));
  }
});

const initialState = {
  isLoggedIn: false,
  isLoggingOut: false,
  logoutError: null as string | null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    login(state) {
      state.isLoggedIn = true;
    }
  },
  extraReducers(builder) {
    builder
      .addCase(performLogout.pending, (state) => {
        state.isLoggingOut = true;
        state.logoutError = null;
      })
      .addCase(performLogout.fulfilled, (state) => {
        state.isLoggingOut = false;
        state.isLoggedIn = false;
      })
      .addCase(performLogout.rejected, (state, action) => {
        state.isLoggingOut = false;
        state.logoutError = action.payload as string || 'Logout failed';
      });
  },
});

export const { login } = authSlice.actions;
export default authSlice.reducer;