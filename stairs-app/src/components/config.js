import React,{ useState, useEffect } from 'react';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Slider from '@mui/material/Slider';
import Select from '@mui/material/Select';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';
import * as CST from '../constants/configs';
import axios from 'axios';

let initialConfigValues = {
  "top_sensor":0,
  "bottom_sensor":0,
  "color_scheme":"default",
  "brightness":100
}

export default function Config() {
  const [error, setError] = useState('');
  const [configData, setConfigData] = useState(initialConfigValues);

  useEffect(() => {
    async function fetchData() {
        await axios(CST.PICO_URL+'/status').then(response => {
        response = response.data
        if (!('color_scheme' in response)) response.color_scheme = "default"
        console.log(response);
        setConfigData(response)
      }).catch(e => {
        console.log(e)
      });
    }
    fetchData();
  },[]);

  function handleChange(e) {
    console.log(e.target.name)
    let data = {};
    data = JSON.parse(JSON.stringify(configData))
    data[e.target.name] = e.target.value;
    console.log(data)
    setConfigData(data);
  }

  function handleUpdateConfig(e) {
    axios.post(CST.PICO_URL+'/config', configData).then(response => {
        console.log(response);
    }).catch((error) => { // error is handled in catch block
      if (error.response) { // status code out of the range of 2xx
        console.log("Data :" , error.response.data);
        console.log("Status :" + error.response.status);
      } else if (error.request) { // The request was made but no response was received
        console.log(error.request);
        setError("Pico offline")
      } else {// Error on setting up the request
        console.log('Error', error.message);
      }
    })
  }

  return (
    <Stack spacing={2} direction="column">
      {error!='' && <Alert severity="error">This is an error alert — check it out!</Alert>}
       <TextField
          name="bottom_sensor"
          label="Bottom sensor distance"
          defaultValue="50"
          value={configData.bottom_sensor}
          type="number"
          helperText="Can be between 0-250 cm"
          onChange={handleChange}
          variant="standard"
        />
        <TextField
          name="top_sensor"
          label="Top sensor distance"
          defaultValue="50"
          value={configData.top_sensor}
          type="number"
          helperText="Can be between 0-250 cm"
          onChange={handleChange}
          variant="standard"
        />
        <FormControl variant="standard" sx={{ m: 1, minWidth: 120 }}>
        <InputLabel id="color-scheme-label">Color scheme</InputLabel>
        <Select
          labelId="color-scheme-label"
          id="color_scheme"
          name="color_scheme"
          value={configData.color_scheme}
          onChange={handleChange}
          label="Color scheme"
        >
          <MenuItem value="">
            <em>None</em>
          </MenuItem>
          <MenuItem value="default">Default</MenuItem>
          <MenuItem value="xmas">Xmas</MenuItem>
          <MenuItem value="panic">Panic</MenuItem>
        </Select>
      </FormControl>
      <Slider aria-label="Brightness" name="brightness" valueLabelDisplay="auto" marks min={0} max={255} value={configData.brightness} onChange={handleChange} />
        <Button onClick={handleUpdateConfig}>Update</Button>
    </Stack>
  );
}