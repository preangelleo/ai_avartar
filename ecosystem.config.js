module.exports = {
  apps: [{
    name: "fanbook",
    script: "/root/src/bot/fanbook/fanbook_bot.py",
    interpreter: "python3",
    env: {
      PYTHONPATH: "/root"
    }
  }]
};
