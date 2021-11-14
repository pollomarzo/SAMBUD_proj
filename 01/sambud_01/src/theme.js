import React from 'react';
import { createTheme, ThemeProvider } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';
import { orange, pink } from '@mui/material/colors';

const theme = createTheme({
    palette: {
        type: 'dark',
    },
});

const AppThemeProvider = ({ children }) => (
    <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
    </ThemeProvider>
);

export default AppThemeProvider;
