import * as React from 'react';
import Switch from '@mui/material/Switch';
import FormControlLabel from '@mui/material/FormControlLabel';

import FormLabel from '@mui/material/FormLabel';

export default function FormControlLabelPosition(props) {
  return (
    <FormControlLabel
        value="start"
        control={<Switch size='small' color="primary" />}
        label={props.data.name}
        labelPlacement="end"
    />
  );
}
