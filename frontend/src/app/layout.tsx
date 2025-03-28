import * as React from 'react';
import AppTheme from '../components/shared-theme/AppTheme';
import AppAppBar from '../components/AppAppBar';
import Box from '@mui/material/Box';
import Script from 'next/script';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <Script
          src={`https://maps.googleapis.com/maps/api/js?key=${process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY}&libraries=places,marker&v=beta`}
          strategy="beforeInteractive"
        />
      </head>
      <body suppressHydrationWarning style={{ margin: 0, padding: 0 }}>
        <AppTheme>
          <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <AppAppBar />
            <Box 
              component="main" 
              sx={{ 
                mt: { xs: '64px', sm: '72px' }, // AppBar height + padding
                flexGrow: 1,
                width: '100%',
                position: 'relative',
                zIndex: 1
              }}
            >
              {children}
            </Box>
          </Box>
        </AppTheme>
      </body>
    </html>
  );
}
