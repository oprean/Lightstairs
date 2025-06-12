import React from 'react'
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
/**
 * this demo uses EMQX Public MQTT Broker (https://www.emqx.com/en/mqtt/public-mqtt5-broker), here are the details:
 *
 * Broker host: broker.emqx.io
 * WebSocket port: 8083
 * WebSocket over TLS/SSL port: 8084
 */

const Connection = ({ connect, disconnect, connectBtn }) => {

  const initialConnectionOptions = {
    // ws or wss
    protocol: 'ws',
    host: 'broker.emqx.io',
    clientId: 'emqx_react_' + Math.random().toString(16).substring(2, 8),
    // ws -> 8083; wss -> 8084
    port: 8083,
    /**
     * By default, EMQX allows clients to connect without authentication.
     * https://docs.emqx.com/en/enterprise/v4.4/advanced/auth.html#anonymous-login
     */
    username: 'emqx_test',
    password: 'emqx_test',
  }

  const handleConnect = () => {
    const { protocol, host, clientId, port, username, password } = initialConnectionOptions
    const url = `${protocol}://${host}:${port}/mqtt`
    const options = {
      clientId,
      username,
      password,
      clean: true,
      reconnectPeriod: 1000, // ms
      connectTimeout: 30 * 1000, // ms
    }
    connect(url, options)
  }

  const handleDisconnect = () => {
    disconnect()
  }

  return (
    <Stack spacing={2} direction="row">
      <Button type="primary" onClick={handleConnect}>
          {connectBtn}
      </Button>
      <Button danger onClick={handleDisconnect}>
         Disconnect
      </Button>
  </Stack>      
  )
}

export default Connection
