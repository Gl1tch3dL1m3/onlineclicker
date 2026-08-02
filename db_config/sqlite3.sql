CREATE TABLE IF NOT EXISTS "bans" (
  "discord_id" INTEGER NOT NULL,
  "reason" TEXT DEFAULT NULL,
  PRIMARY KEY ("discord_id")
);

CREATE TABLE IF NOT EXISTS "chatlogs" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "username" TEXT NOT NULL,
  "message" TEXT NOT NULL,
  "node" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "logs" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "executor" INTEGER NOT NULL,
  "target" INTEGER DEFAULT NULL,
  "action" TEXT DEFAULT NULL,
  "note" TEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS "players" (
  "discord_id" INTEGER NOT NULL,
  "username" TEXT NOT NULL,
  "password" TEXT DEFAULT NULL,
  "nickname_color" INTEGER DEFAULT NULL,
  PRIMARY KEY ("discord_id")
);
