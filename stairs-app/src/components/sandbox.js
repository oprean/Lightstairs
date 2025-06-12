import React,{ useState, useEffect } from 'react';
import Stack from '@mui/material/Stack';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import * as CST from '../constants/configs';
import axios from 'axios';
//import { Box } from '@mui/material';
axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';

export default function Sandbox() {
  const [temperature, setTemperature] = useState(0);
  function handle_reset() {
    axios.get(CST.PICO_URL+'/reset').then(response => {
        console.log(response);
    })
  }

  function handle_temperature() {
    axios.get(CST.PICO_URL+'/temperature').then(response => {
      setTemperature(response.data.onboard_temperature);
    })
  }

  return (
    <Stack spacing={2} direction="column">
      <Typography variant="h1" gutterBottom>
        {temperature} C
      </Typography>
      <Button variant="text" onClick={handle_reset}>reset</Button>
      <Button variant="text" onClick={handle_temperature}>temperature</Button>
    </Stack>
  );
}