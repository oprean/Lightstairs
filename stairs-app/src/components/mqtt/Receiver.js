import React, { useEffect, useState } from 'react';
import Stack from '@mui/material/Stack';

const Receiver = ({ payload }) => {
  const [messages, setMessages] = useState([])

  useEffect(() => {
    if (payload.topic) {
      setMessages(messages => [...messages, payload])
    }
  }, [payload])

  return (
    <Stack spacing={2} direction="column" alignContent="left">
      {messages.map((item,i) => {
        return <div key={i}>{item.topic} : {item.message}</div>
      })}
    </Stack>
  );
}

export default Receiver;
