//https://picow.pinout.xyz/
import * as React from 'react';
import { ReactComponent as YourSvg } from './raspberry-pi-picow.svg';
import Grid from '@mui/material/Grid';
import * as PICO from '../constants/picopins';
import Pin from './pin';
export default function SimplePaper() {
  return (
    <Grid container spacing={0}>
        <Grid item xs={2}>
        {PICO.PINS.filter(pin => pin.physical<=20).map((pin,i) => {
           return <Grid item xs={12} style={{textAlign:'left'}}><Pin data={pin}/></Grid>
        })}
        </Grid>
        <Grid item xs={6}>
            <YourSvg/>
        </Grid>
        <Grid item xs={4}>
        {PICO.PINS.filter(pin => pin.physical>20).map((pin,i) => {
           return <Grid item xs={12} style={{textAlign:'left'}}><Pin data={pin}/></Grid>

        })}
        </Grid>
    </Grid>

  );
}