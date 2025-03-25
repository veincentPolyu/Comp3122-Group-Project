'use client';

import * as React from 'react';
import { experimental_extendTheme as extendTheme } from '@mui/material/styles';
import { Experimental_CssVarsProvider as CssVarsProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const theme = extendTheme({
  colorSchemes: {
    light: {
      palette: {
        primary: {
          main: '#1976d2',
        },
        secondary: {
          main: '#dc004e',
        },
      },
    },
    dark: {
      palette: {
        primary: {
          main: '#90caf9',
        },
        secondary: {
          main: '#f48fb1',
        },
      },
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          scrollBehavior: 'smooth',
          '& button, & a': {
            transition: 'all 0.2s ease-in-out',
          },
        },
      },
    },
  },
});

export default function AppTheme({ children }: { children: React.ReactNode }) {
  const [disableTransition, setDisableTransition] = React.useState(false);

  return (
    <CssVarsProvider
      theme={theme}
      defaultMode="system"
      disableTransitionOnChange={disableTransition}
    >
      <CssBaseline />
      {children}
    </CssVarsProvider>
  );
}