-- Usuarios de prueba
INSERT INTO user (user_name, user_password, token, is_active, created_by, created_at)
VALUES
  ('admin@test.com', 'hashed_admin', 'token_admin', 1, 1, NOW()),
  ('user1@test.com', 'hashed_user1', 'token_user1', 1, 1, NOW());

-- Notificaciones de prueba
INSERT INTO notifications (sender_id, receiver_id, sender_contact, receiver_contact,
  subject, message, channel, status, created_by, created_at)
VALUES
  (1, 2, 'admin@test.com', 'user1@test.com', 'Test Subject', 'Test Message', 'email', 'pending', 1, NOW());