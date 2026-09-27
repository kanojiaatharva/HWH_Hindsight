module.exports = {
  apps: [
    {
      name: 'hindsight-backend',
      cwd: './backend',
      script: 'start.cjs',
      interpreter: 'C:/Program Files/nodejs/node.exe',
      env: {
        NODE_ENV: 'development',
        PYTHONUNBUFFERED: '1'
      }
    },
    {
      name: 'hindsight-frontend',
      cwd: './frontend',
      script: 'node_modules/next/dist/bin/next',
      args: 'dev -p 3001',
      interpreter: 'C:/Program Files/nodejs/node.exe',
      env: {
        NODE_ENV: 'development'
      }
    }
  ]
};