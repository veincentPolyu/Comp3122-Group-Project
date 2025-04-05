'use client';

import * as React from 'react';
import DarkModeIcon from '@mui/icons-material/DarkModeRounded';
import LightModeIcon from '@mui/icons-material/LightModeRounded';
import IconButton, { IconButtonOwnProps } from '@mui/material/IconButton';
import { useColorScheme } from '@mui/material/styles';

export default function ColorModeIconDropdown(props: IconButtonOwnProps) {
  const { mode, setMode } = useColorScheme();

  const toggleColorMode = () => {
    setMode(mode === 'light' ? 'dark' : 'light');
  };

  const icon = mode === 'light' ? <DarkModeIcon /> : <LightModeIcon />;

  return (
    <IconButton
      onClick={toggleColorMode}
      aria-label={`Switch to ${mode === 'light' ? 'dark' : 'light'} mode`}
      {...props}
    >
      {icon}
    </IconButton>
  );
}