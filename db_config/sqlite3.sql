CREATE TABLE IF NOT EXISTS "players" (
  "discord_id" INTEGER NOT NULL,
  "username" TEXT NOT NULL,
  "password" TEXT DEFAULT NULL,
  "nickname_color" INTEGER DEFAULT NULL,
  "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("discord_id")
);

CREATE TABLE IF NOT EXISTS "bans" (
  "discord_id" INTEGER NOT NULL,
  "reason" TEXT DEFAULT NULL,
  "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY ("discord_id")
);

CREATE TABLE IF NOT EXISTS "chatlogs" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "username" TEXT NOT NULL,
  "message" TEXT NOT NULL,
  "node" TEXT NOT NULL,
  "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "logs" (
  "id" INTEGER PRIMARY KEY AUTOINCREMENT,
  "executor" INTEGER NOT NULL,
  "target" INTEGER DEFAULT NULL,
  "action" TEXT DEFAULT NULL,
  "note" TEXT DEFAULT NULL,
  "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS "idx_chatlogs_username_time" ON "chatlogs" ("username", "created_at");
CREATE INDEX IF NOT EXISTS "idx_chatlogs_created_at" ON "chatlogs" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_logs_executor" ON "logs" ("executor");
CREATE INDEX IF NOT EXISTS "idx_logs_target" ON "logs" ("target");
CREATE INDEX IF NOT EXISTS "idx_logs_created_at" ON "logs" ("created_at");