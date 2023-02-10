import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

export default function Navbar() {
  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            หน้าหลัก
          </Typography>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            สายงานบัณฑิต
          </Typography>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            พยากรนักศึกษา
          </Typography>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            แนะนำวิชาเลือก
          </Typography>
          <Button><Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>เข้าสู่ระบบ</Typography></Button>
        </Toolbar>
      </AppBar>
    </Box>
  );
}