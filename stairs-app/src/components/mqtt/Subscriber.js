import React, { useContext } from 'react'
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';

import { QosOption } from './index'

const Subscriber = ({ sub, unSub, showUnsub }) => {
  const qosOptions = useContext(QosOption)

  // topic & QoS for MQTT subscribing
  const record = {
    topic: 'raspberry/mqtt',
    qos: 0,
  }

  const handleSub = () => {
    sub(record)
  }

  const handleUnsub = () => {
    unSub(record)
  }


  return (
    <Stack spacing={2} direction="row">
      <Button type="primary" onClick={handleSub}>Subscribe</Button>
      {showUnsub ? (
        <Button
          type="danger"
          style={{ marginLeft: '10px' }}
          onClick={handleUnsub}
        >
          Unsubscribe
        </Button>
      ) : null}
    </Stack>
  )
}

export default Subscriber
