import * as React from 'react';
import AppTheme from '../components/shared-theme/AppTheme';
import AppAppBar from '../components/AppAppBar';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <AppTheme>
          <AppAppBar />
          {children}
        </AppTheme>
      </body>
    </html>
  );
}
