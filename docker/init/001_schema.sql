CREATE TABLE user(
    id_user INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL,
    user_password VARCHAR(255) NOT NULL,
    token TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_by INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_by INT,
    deleted_at TIMESTAMP
);

CREATE TABLE notifications(
    id_notification INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    sender_contact VARCHAR(255),
    receiver_contact VARCHAR(255),
    subject VARCHAR(255),
    message TEXT,
    channel ENUM('email','sms','push'),
    status ENUM('pending','sent','failed'),
    created_by INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_by INT,
    deleted_at TIMESTAMP
)