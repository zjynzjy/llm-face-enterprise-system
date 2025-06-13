/*
 Navicat Premium Data Transfer

 Source Server         : localhost_3306
 Source Server Type    : MySQL
 Source Server Version : 80028
 Source Host           : localhost:3306
 Source Schema         : db_admin2

 Target Server Type    : MySQL
 Target Server Version : 80028
 File Encoding         : 65001

 Date: 13/06/2025 16:41:09
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `group_id` int(0) NOT NULL,
  `permission_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `content_type_id` int(0) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 64 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add permission', 1, 'add_permission');
INSERT INTO `auth_permission` VALUES (2, 'Can change permission', 1, 'change_permission');
INSERT INTO `auth_permission` VALUES (3, 'Can delete permission', 1, 'delete_permission');
INSERT INTO `auth_permission` VALUES (4, 'Can view permission', 1, 'view_permission');
INSERT INTO `auth_permission` VALUES (5, 'Can add group', 2, 'add_group');
INSERT INTO `auth_permission` VALUES (6, 'Can change group', 2, 'change_group');
INSERT INTO `auth_permission` VALUES (7, 'Can delete group', 2, 'delete_group');
INSERT INTO `auth_permission` VALUES (8, 'Can view group', 2, 'view_group');
INSERT INTO `auth_permission` VALUES (9, 'Can add user', 3, 'add_user');
INSERT INTO `auth_permission` VALUES (10, 'Can change user', 3, 'change_user');
INSERT INTO `auth_permission` VALUES (11, 'Can delete user', 3, 'delete_user');
INSERT INTO `auth_permission` VALUES (12, 'Can view user', 3, 'view_user');
INSERT INTO `auth_permission` VALUES (13, 'Can add content type', 4, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (14, 'Can change content type', 4, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (15, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (16, 'Can view content type', 4, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (17, 'Can add session', 5, 'add_session');
INSERT INTO `auth_permission` VALUES (18, 'Can change session', 5, 'change_session');
INSERT INTO `auth_permission` VALUES (19, 'Can delete session', 5, 'delete_session');
INSERT INTO `auth_permission` VALUES (20, 'Can view session', 5, 'view_session');
INSERT INTO `auth_permission` VALUES (21, 'Can add sys user', 6, 'add_sysuser');
INSERT INTO `auth_permission` VALUES (22, 'Can change sys user', 6, 'change_sysuser');
INSERT INTO `auth_permission` VALUES (23, 'Can delete sys user', 6, 'delete_sysuser');
INSERT INTO `auth_permission` VALUES (24, 'Can view sys user', 6, 'view_sysuser');
INSERT INTO `auth_permission` VALUES (25, 'Can add sys role', 7, 'add_sysrole');
INSERT INTO `auth_permission` VALUES (26, 'Can change sys role', 7, 'change_sysrole');
INSERT INTO `auth_permission` VALUES (27, 'Can delete sys role', 7, 'delete_sysrole');
INSERT INTO `auth_permission` VALUES (28, 'Can view sys role', 7, 'view_sysrole');
INSERT INTO `auth_permission` VALUES (29, 'Can add sys user role', 8, 'add_sysuserrole');
INSERT INTO `auth_permission` VALUES (30, 'Can change sys user role', 8, 'change_sysuserrole');
INSERT INTO `auth_permission` VALUES (31, 'Can delete sys user role', 8, 'delete_sysuserrole');
INSERT INTO `auth_permission` VALUES (32, 'Can view sys user role', 8, 'view_sysuserrole');
INSERT INTO `auth_permission` VALUES (33, 'Can add sys menu', 9, 'add_sysmenu');
INSERT INTO `auth_permission` VALUES (34, 'Can change sys menu', 9, 'change_sysmenu');
INSERT INTO `auth_permission` VALUES (35, 'Can delete sys menu', 9, 'delete_sysmenu');
INSERT INTO `auth_permission` VALUES (36, 'Can view sys menu', 9, 'view_sysmenu');
INSERT INTO `auth_permission` VALUES (37, 'Can add sys role menu', 10, 'add_sysrolemenu');
INSERT INTO `auth_permission` VALUES (38, 'Can change sys role menu', 10, 'change_sysrolemenu');
INSERT INTO `auth_permission` VALUES (39, 'Can delete sys role menu', 10, 'delete_sysrolemenu');
INSERT INTO `auth_permission` VALUES (40, 'Can view sys role menu', 10, 'view_sysrolemenu');
INSERT INTO `auth_permission` VALUES (41, 'Can add sys company location', 11, 'add_syscompanylocation');
INSERT INTO `auth_permission` VALUES (42, 'Can change sys company location', 11, 'change_syscompanylocation');
INSERT INTO `auth_permission` VALUES (43, 'Can delete sys company location', 11, 'delete_syscompanylocation');
INSERT INTO `auth_permission` VALUES (44, 'Can view sys company location', 11, 'view_syscompanylocation');
INSERT INTO `auth_permission` VALUES (45, 'Can add sys face feature', 12, 'add_sysfacefeature');
INSERT INTO `auth_permission` VALUES (46, 'Can change sys face feature', 12, 'change_sysfacefeature');
INSERT INTO `auth_permission` VALUES (47, 'Can delete sys face feature', 12, 'delete_sysfacefeature');
INSERT INTO `auth_permission` VALUES (48, 'Can view sys face feature', 12, 'view_sysfacefeature');
INSERT INTO `auth_permission` VALUES (49, 'Can add sys attendance', 13, 'add_sysattendance');
INSERT INTO `auth_permission` VALUES (50, 'Can change sys attendance', 13, 'change_sysattendance');
INSERT INTO `auth_permission` VALUES (51, 'Can delete sys attendance', 13, 'delete_sysattendance');
INSERT INTO `auth_permission` VALUES (52, 'Can view sys attendance', 13, 'view_sysattendance');
INSERT INTO `auth_permission` VALUES (53, 'Can add 安全日志', 14, 'add_syssecuritylog');
INSERT INTO `auth_permission` VALUES (54, 'Can change 安全日志', 14, 'change_syssecuritylog');
INSERT INTO `auth_permission` VALUES (55, 'Can delete 安全日志', 14, 'delete_syssecuritylog');
INSERT INTO `auth_permission` VALUES (56, 'Can view 安全日志', 14, 'view_syssecuritylog');
INSERT INTO `auth_permission` VALUES (57, 'Can add sys department', 15, 'add_sysdepartment');
INSERT INTO `auth_permission` VALUES (58, 'Can change sys department', 15, 'change_sysdepartment');
INSERT INTO `auth_permission` VALUES (59, 'Can delete sys department', 15, 'delete_sysdepartment');
INSERT INTO `auth_permission` VALUES (60, 'Can view sys department', 15, 'view_sysdepartment');
INSERT INTO `auth_permission` VALUES (61, 'Can add sys user department', 16, 'add_sysuserdepartment');
INSERT INTO `auth_permission` VALUES (62, 'Can change sys user department', 16, 'change_sysuserdepartment');
INSERT INTO `auth_permission` VALUES (63, 'Can delete sys user department', 16, 'delete_sysuserdepartment');
INSERT INTO `auth_permission` VALUES (64, 'Can view sys user department', 16, 'view_sysuserdepartment');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `first_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `last_name` varchar(150) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `email` varchar(254) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `user_id` int(0) NOT NULL,
  `group_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_groups_user_id_group_id_94350c0c_uniq`(`user_id`, `group_id`) USING BTREE,
  INDEX `auth_user_groups_group_id_97559544_fk_auth_group_id`(`group_id`) USING BTREE,
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `user_id` int(0) NOT NULL,
  `permission_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq`(`user_id`, `permission_id`) USING BTREE,
  INDEX `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (2, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (1, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'user');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (15, 'datascreen', 'sysdepartment');
INSERT INTO `django_content_type` VALUES (16, 'datascreen', 'sysuserdepartment');
INSERT INTO `django_content_type` VALUES (13, 'face', 'sysattendance');
INSERT INTO `django_content_type` VALUES (11, 'face', 'syscompanylocation');
INSERT INTO `django_content_type` VALUES (12, 'face', 'sysfacefeature');
INSERT INTO `django_content_type` VALUES (14, 'face', 'syssecuritylog');
INSERT INTO `django_content_type` VALUES (9, 'menu', 'sysmenu');
INSERT INTO `django_content_type` VALUES (10, 'menu', 'sysrolemenu');
INSERT INTO `django_content_type` VALUES (7, 'role', 'sysrole');
INSERT INTO `django_content_type` VALUES (8, 'role', 'sysuserrole');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (6, 'user', 'sysuser');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (1, 'user', '0001_initial', '2025-02-14 07:58:27.916474');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0001_initial', '2025-02-19 02:48:36.084136');
INSERT INTO `django_migrations` VALUES (3, 'contenttypes', '0002_remove_content_type_name', '2025-02-19 02:48:36.141968');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0001_initial', '2025-02-19 02:48:36.541803');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0002_alter_permission_name_max_length', '2025-02-19 02:48:36.601583');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0003_alter_user_email_max_length', '2025-02-19 02:48:36.652739');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0004_alter_user_username_opts', '2025-02-19 02:48:36.658147');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0005_alter_user_last_login_null', '2025-02-19 02:48:36.694348');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0006_require_contenttypes_0002', '2025-02-19 02:48:36.696657');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0007_alter_validators_add_error_messages', '2025-02-19 02:48:36.701365');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0008_alter_user_username_max_length', '2025-02-19 02:48:36.744592');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0009_alter_user_last_name_max_length', '2025-02-19 02:48:36.791945');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0010_alter_group_name_max_length', '2025-02-19 02:48:36.809057');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0011_update_proxy_permissions', '2025-02-19 02:48:36.816564');
INSERT INTO `django_migrations` VALUES (15, 'auth', '0012_alter_user_first_name_max_length', '2025-02-19 02:48:36.882013');
INSERT INTO `django_migrations` VALUES (16, 'role', '0001_initial', '2025-02-19 02:48:36.984752');
INSERT INTO `django_migrations` VALUES (17, 'menu', '0001_initial', '2025-02-19 02:48:37.057965');
INSERT INTO `django_migrations` VALUES (18, 'menu', '0002_initial', '2025-02-19 02:48:37.098232');
INSERT INTO `django_migrations` VALUES (19, 'sessions', '0001_initial', '2025-02-19 02:48:37.125346');
INSERT INTO `django_migrations` VALUES (20, 'face', '0001_initial', '2025-03-02 09:27:52.647988');
INSERT INTO `django_migrations` VALUES (21, 'datascreen', '0001_initial', '2025-03-27 09:50:20.573866');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sys_attendance
-- ----------------------------
DROP TABLE IF EXISTS `sys_attendance`;
CREATE TABLE `sys_attendance`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `check_time` datetime(6) NOT NULL,
  `location` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `accuracy` double NOT NULL,
  `is_valid` tinyint(1) NOT NULL,
  `face_match_score` double NOT NULL,
  `device_info` json NOT NULL,
  `user_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sys_attenda_user_id_606208_idx`(`user_id`, `check_time`) USING BTREE,
  CONSTRAINT `sys_attendance_user_id_0692846a_fk_sys_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 59 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_attendance
-- ----------------------------
INSERT INTO `sys_attendance` VALUES (1, '2025-03-28 04:00:08.000000', '30.2672,-97.7431', 98.5, 1, 0.969116747379303, '{\"device_id\": \"12345\", \"device_type\": \"mobile\"}', 1);
INSERT INTO `sys_attendance` VALUES (34, '2025-03-27 10:24:13.623017', '24.0910336,120.5665792', 4500.673662471836, 1, 0.9972606301307678, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"}', 18);
INSERT INTO `sys_attendance` VALUES (35, '2025-03-27 10:24:59.196921', '24.0910336,120.5665792', 4500.673662471836, 1, 0.9918270707130432, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"}', 21);
INSERT INTO `sys_attendance` VALUES (36, '2025-03-27 10:25:57.786887', '24.0910336,120.5665792', 4500.673662471836, 1, 0.9907737374305725, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"}', 19);
INSERT INTO `sys_attendance` VALUES (41, '2025-03-27 10:32:06.754301', '24.0910336,120.5665792', 4500.673662471836, 1, 0.9232752919197083, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"}', 19);
INSERT INTO `sys_attendance` VALUES (42, '2025-03-28 10:44:15.000000', '24.0910336,120.5665792', 4500.673662471836, 1, 0.9909831881523132, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"}', 20);
INSERT INTO `sys_attendance` VALUES (43, '2025-03-29 04:31:46.447892', '39.9042,116.4074', 10000, 1, 0.9532304406166077, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"}', 1);
INSERT INTO `sys_attendance` VALUES (44, '2025-04-01 05:07:04.514309', '39.9042,116.4074', 10000, 1, 0.9671515226364136, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"}', 1);
INSERT INTO `sys_attendance` VALUES (45, '2025-04-01 05:38:53.752472', '39.9042,116.4074', 10000, 1, 0.9755713939666748, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"}', 1);
INSERT INTO `sys_attendance` VALUES (46, '2025-04-05 04:31:33.073692', '39.9042,116.4074', 10000, 1, 0.9618682861328125, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"}', 1);
INSERT INTO `sys_attendance` VALUES (47, '2025-04-05 04:32:04.110112', '39.9042,116.4074', 10000, 1, 0.964981198310852, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"}', 1);
INSERT INTO `sys_attendance` VALUES (48, '2025-04-07 13:57:44.430720', '39.9042,116.4074', 10000, 1, 0.9632681608200073, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"}', 1);
INSERT INTO `sys_attendance` VALUES (49, '2025-04-07 14:04:11.132259', '39.9042,116.4074', 10000, 1, 0.9578603506088257, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36\"}', 1);
INSERT INTO `sys_attendance` VALUES (50, '2025-04-19 03:32:10.958260', '24.0779264,120.537088', 2582.1420170493816, 1, 0.9709546566009521, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36\"}', 1);
INSERT INTO `sys_attendance` VALUES (51, '2025-04-19 03:34:27.045513', '34.74976440102083,113.61079146586465', 63, 1, 0.9644854664802551, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0\"}', 1);
INSERT INTO `sys_attendance` VALUES (52, '2025-04-19 03:36:51.267594', '34.74976440102083,113.61079146586465', 63, 1, 0.9719269871711731, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0\"}', 1);
INSERT INTO `sys_attendance` VALUES (53, '2025-04-20 02:48:17.738486', '34.74977134728619,113.61063663402689', 55, 1, 0.9649100303649902, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0\"}', 1);
INSERT INTO `sys_attendance` VALUES (54, '2025-04-20 02:50:21.414940', '34.74977134728619,113.61063663402689', 55, 0, 0.9641643166542053, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0\"}', 1);
INSERT INTO `sys_attendance` VALUES (55, '2025-04-29 03:24:11.082137', '34.7948,113.6906', 50000, 1, 0.9726539254188538, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0\"}', 1);
INSERT INTO `sys_attendance` VALUES (56, '2025-04-29 03:36:37.905505', '34.7948,113.6906', 50000, 1, 0.9664178490638733, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0\"}', 1);
INSERT INTO `sys_attendance` VALUES (57, '2025-05-10 21:54:54.011910', '24.1634,120.6467', 30710, 1, 0.9735416769981384, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0\"}', 1);
INSERT INTO `sys_attendance` VALUES (58, '2025-05-12 21:30:24.545179', '24.0517963,120.5161352', 20312.83603724693, 1, 0.9598566889762878, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36\"}', 1);
INSERT INTO `sys_attendance` VALUES (59, '2025-05-13 14:47:25.853507', '39.9042,116.4074', 10000, 1, 0.9569205045700073, '{\"platform\": \"Win32\", \"userAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36\"}', 1);

-- ----------------------------
-- Table structure for sys_company_location
-- ----------------------------
DROP TABLE IF EXISTS `sys_company_location`;
CREATE TABLE `sys_company_location`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `latitude` decimal(9, 6) NOT NULL,
  `longitude` decimal(9, 6) NOT NULL,
  `radius` int(0) UNSIGNED NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for sys_department
-- ----------------------------
DROP TABLE IF EXISTS `sys_department`;
CREATE TABLE `sys_department`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `latitude` decimal(9, 6) NOT NULL,
  `longitude` decimal(9, 6) NOT NULL,
  `radius` int(0) UNSIGNED NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_department
-- ----------------------------
INSERT INTO `sys_department` VALUES (1, '研发部', 39.904200, 116.407400, 1000, 1);
INSERT INTO `sys_department` VALUES (2, '市场部', 34.586034, 113.685730, 1000, 1);
INSERT INTO `sys_department` VALUES (3, '财务部', 39.990479, 116.296511, 1000, 1);
INSERT INTO `sys_department` VALUES (4, '人事部', 39.987429, 116.162995, 1000, 1);

-- ----------------------------
-- Table structure for sys_face_feature
-- ----------------------------
DROP TABLE IF EXISTS `sys_face_feature`;
CREATE TABLE `sys_face_feature`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `feature` longblob NOT NULL,
  `create_time` datetime(6) NOT NULL,
  `user_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id`) USING BTREE,
  CONSTRAINT `sys_face_feature_user_id_412b9ae9_fk_sys_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_face_feature
-- ----------------------------
INSERT INTO `sys_face_feature` VALUES (2, 0x8004958C020000000000008C166E756D70792E5F636F72652E6D756C74696172726179948C0C5F7265636F6E7374727563749493948C056E756D7079948C076E6461727261799493944B0085944301629487945294284B014B80859468038C0564747970659493948C02663494898887945294284B038C013C944E4E4E4AFFFFFFFF4AFFFFFFFF4B007494628942000200002239A5BD96B9BB3D677E343CA864BEBBCAA056BDB783DABCD410DFBDFA5909BE90DC023EFC881ABD7BDF333E10BB18BD711B2DBE7B7AAABDA5646DBD1C06D53DF3EC45BEC8DDFFBD28095CBC10EC7CBD5BD91D3D93420D3C36BE003DCED0123D0930D1BDBB42ACBE568796BD9178CFBD25B2C13DEAC99ABC7EAC4CBD9E48FFBA5C5A76BE5D29D4BDC6639B3D6545A63D9CEAA1BBCDB88F3891446E3E1B45F1BC8BAF2CBEEB1F0D3C8503B03D91B9783EF7A72A3E45B70E3E84D912BC1AC444BE5F2CFA3D002BE6BD0881B93D6A21563E0B11663D8AD5A23DE7736EBDBF290BBE680B553DBE639D3D56DF3ABE0A4FD13CD632C13DF1716FBDDF4811BD66BD0CBDB7EA8E3E1DF47A3D050DCDBD166941BEC610F63D7E973DBE42CBA6BD36DCFB3C85BEB0BD43BC06BE044BB6BE57FB653C07C6D63ED2F38D3D55882ABEC066BC3D8F777CBD2BB294BD67EC1C3EE812283E4191CDBD854F0F3D52A1A0BC274479BB663E663E9E05CD3B950DF6BC9B78193EE66DCFBAD6F5D23D78F2883D816E9D3D8724E2BDF24FA43CAAFF15BEAA72CBBCEB96413D9E783F3CC422833D24ED1C3E849945BEF3B2083ED1A3393CF73DA3BC4F02883DE32C4CBA678D97BDDEB609BE912B153EF9C877BEA5D8683E050C143E8033BB3DACB51C3EFB2A0B3E728DE73DD280DABBB3E6D13CDC5D5BBEBB5274BC4127893DE2DA49BDD10CF83D13FBA03C947494622E, '2025-03-26 14:55:57.615727', 1);
INSERT INTO `sys_face_feature` VALUES (3, 0x8004958C020000000000008C166E756D70792E5F636F72652E6D756C74696172726179948C0C5F7265636F6E7374727563749493948C056E756D7079948C076E6461727261799493944B0085944301629487945294284B014B80859468038C0564747970659493948C02663494898887945294284B038C013C944E4E4E4AFFFFFFFF4AFFFFFFFF4B0074946289420002000063DEF5BDA704C23DE4940ABD52CD62BDEF8D8BBDB5801ABD10A0D8BD49DFBDBDD8D6D63D0804EABCF90A743E40C1B1BD54D85BBE39A1E6BDC62687BDC61E0F3EF7B933BE7752FCBD99EAAEBC280110BD8243693D4609043D8FBFD73C8E43A23DA67E7DBD60F19CBE1A6F84BD7386BEBDBCF97E3DD49D33BDCF142EBD159D22BCE90F66BEAF45A7BD09C0953D1C96993D5CF20DBCCBCDAEBCA2F0743E3E4128BDDC9D38BE246EA4BCBDA0D63DBFBB853E92ED243ED0BEA53D26D1A43B5B5025BE0A26B43DEE45AFBD3EB91E3D26056A3E3DDDF53DE9212A3DD6A981BD21ADF7BDAAC0683D57B9FC3DF5550BBE29221E3CCC64FF3D806A84BD4EBE23BD377688BD5CA19C3E2929543CC9C903BEAA347DBE1C89EC3DEE1517BE53EDF5BDAFD7913D403B04BE99F714BE560EACBE7241503CAEDFB13E6799933D67813CBE1042143EEDEDAABD49DF0ABD6163DE3D1EE2143ED491A1BD809B233DD2CCDFBDAB3615BD96DE5E3E05D00BBD422C43BC62DB043EF76CAE3A49A1923D293C693D3AAE133D6A4CDFBDFF2AE33C76E5E5BDF00063BC090B163D7FCBCFBCAA0C433DB3A4063E4A502BBED074FB3D6411CABB0679803C1AFDB83C8F1DF23B40F286BD963CE1BD5E71013EE88F6CBEF0D6613EB9C8D43DDA94013EFBE4073E7E3F3C3E0972123E610AE0BC129A2B3D004F5CBEDEA50DBD71A0863D840036BD48E8283E967DD93C947494622E, '2025-03-27 10:23:55.997202', 18);
INSERT INTO `sys_face_feature` VALUES (4, 0x8004958C020000000000008C166E756D70792E5F636F72652E6D756C74696172726179948C0C5F7265636F6E7374727563749493948C056E756D7079948C076E6461727261799493944B0085944301629487945294284B014B80859468038C0564747970659493948C02663494898887945294284B038C013C944E4E4E4AFFFFFFFF4AFFFFFFFF4B00749462894200020000BCC6E0BD4216D03D5E5F46BC97EE67BD740A99BD01243CBD6C54D7BDD2B003BEAE9BF73DC5E501BD79D1653E2B575FBDD1E53ABE235EECBD8075A6BDC99A173E761431BE1F5FF8BDDF19CEBCA46701BD0403813D9B424C3D59C43E3DDB392D3D942492BD5CA18DBEF52447BDF192D9BD905E293DD63194BBE8311ABD0CAC1C3C45844CBE3954B2BD2180C03DA0CB843D908585BCAD94ADBC0E0E503E2FCB39BDADC23EBE7F838BBC8095D63DD7EE783EA9982D3E95BFA13DD618273CB4FB37BE81FCCB3D0524ACBD3609193DFC9F493E9D95A53D3EBA313D89945EBC918C05BE5441A33D732CCF3D5F42ECBDAF07CA3C8FF60A3E84F43DBDDEE740BDB08FA5BD90FD883EDA3F4D3CD421F7BD2FA365BE4ADAC93D11CC0FBE8A1417BEF9776C3D9DCA10BEFFAB1EBE0F67A9BE3ABD1ABDB074AE3E058CC23D74984CBE3135FE3D0E6EF7BCC50B893ABF53163E127F203EC33979BD2A2C5A3DE8F7B0BDA8459ABD2F3A623E9F4F06BDC4DE2DBD224F283ED68733BC67947E3D9523573DD36E963C860E92BDA3D90E3D61D408BEAA34B3BC3E022D3D94E700BD693EF23C1978F23D6E7F27BE4D6DE43D72E2D0BB18B7863D99128A3C9DACECBB408C97BD11B191BDB1080B3EDF9C45BE37CF7B3EFDC9003E4100053E7698F43DC2F6403E4FDDDD3D081998BCA00C3C3D5BE14FBECE464BBD456F643DD3A087BD9CF21D3EAE1B103D947494622E, '2025-03-27 10:24:48.103027', 21);
INSERT INTO `sys_face_feature` VALUES (5, 0x8004958C020000000000008C166E756D70792E5F636F72652E6D756C74696172726179948C0C5F7265636F6E7374727563749493948C056E756D7079948C076E6461727261799493944B0085944301629487945294284B014B80859468038C0564747970659493948C02663494898887945294284B038C013C944E4E4E4AFFFFFFFF4AFFFFFFFF4B007494628942000200009FF508BD2206943D0D2B573DB95DE1BA92C92CBDC250323B4AD875BD38CBD5BD77FBE83D643FB6BD6A536A3EF35D98BD27FD3BBE7DDD18BE9B70EBBCF93C213E6C8F40BE9CC6A7BD928876BDB6E37CBD940BBB3B8015CEBC0E20F23C5624FD3C958B69BD7A4AB5BE198BCBBDFE1C0CBEBA4C973D8BBA9FBD338B17BD81F51BBB0A922CBE672959BD0E2CC8BC11A6B83CFACD37BDD23346BD91A4313EC3AC57BDED3824BE6895AABB56BCEF3C3481543E7291553EE024A03D67A19FBBC49FFCBD7E55F73D488000BE8383553D392B243E683A953DAAA65D3DC5E0243DA0028BBD1C1E963CE2A2963D247E2BBE76CFDB3BD5C6993CD6D71EBDF55E58BD544556BD7F2D4C3E6145863D1FBAADBDA91139BE85C5203E890348BEDED757BDDC3E363DB46CCFBDB6CB20BE8DC1A5BE5C53C13C110BC53E1EF2AC3D806935BED23D773D673E1CBDFA23B8BD914B0C3E68491C3EAFD640BD622D82BC791566BD2CA692BC910F0B3ED23E8FBD0250F4BBF34B333E3AAF48BD2F29BC3C652B173D8320133D7D72B5BDDBC6923DCE69CCBDF59FDDBC8A29D23DA64841BD265D393C7BEA8D3D91340EBEA206003E3E5D1A3C12F59D3C5305B93D6EBB9FBC6B80F2BD03F0C1BD9DB6443EF9B96BBE6C0B2F3E289A133EC7B16D3CA89EEA3DEE70D73D5124223E67B304BD094CE6BC709553BEF2958CBC0EC85D3DA3C808BD1E0A013D2506A3BB947494622E, '2025-03-27 10:25:44.181484', 19);
INSERT INTO `sys_face_feature` VALUES (6, 0x8004958C020000000000008C166E756D70792E5F636F72652E6D756C74696172726179948C0C5F7265636F6E7374727563749493948C056E756D7079948C076E6461727261799493944B0085944301629487945294284B014B80859468038C0564747970659493948C02663494898887945294284B038C013C944E4E4E4AFFFFFFFF4AFFFFFFFF4B007494628942000200003A5629BD7705F13D107634BD65278ABD3D09B3BD868C44BD0A9178BD7129A8BD82DC263E6A0A6CBD3D9E3E3E829496BC8D981CBEF16F15BE435F96BD8697153E54A466BE275B2BBEC9CA3CBD8F01D73C39E5D23D7EE7B13C0BB9363D75A5C33CDE59F1BD65F59CBEB44153BD2D260DBE9668193DF47263BD23489039DD93CE3C6D394EBE74BC3EBD9B9F3A3DCC78773C3BC883BC6E3943BD9858713E6125953C50377FBE63492E3D6407A23C252A753E29D7293E8146593D9A51AF3C411D1DBE209B2D3ED548C5BD0537053D14174B3EEB30D03D49A2253D8C3C4F3C8A4808BEE3C6DF3DD72B323DD745FFBD654739BD498EAB3DD49D9CBC2A784C3C32CC33BD166A4D3EA9C973BDAE4C85BD6CB23DBE475CEF3D3DA701BE9F37AEBDC6E5D13D6A8612BE2AEE24BE3E9993BE8B889CBC7791B83E96FD023EA88B3FBE09BA963DD8BA8DBDEFE30BBC8FD7F23D01DDFF3DD50CA8BD4A3D7A3D9DC313BED5AF44BD72FE683ECA7F92BDB9C039BD83D2403ED0BE273DE233903DD08BBE3CA0A17ABDD962A0BD01AB883DD51FC0BD4EC811BC51435C3D93636BBC663D00BDEAF90D3EE8C519BEBDB8B33D7E913FBBB444B33C43D92DBD4DA8C83CC389C6BDD922D5BD4649B33DE6DB29BE9101493E0FCF163EC6E1DF3D67FFC93DDDCB1F3EFC238C3D610186BD2667023B9E0358BE86E520BD4B2EDA3D9C3031BB7CD5EE3D204BC2BB947494622E, '2025-03-27 10:44:03.759251', 20);

-- ----------------------------
-- Table structure for sys_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `icon` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `parent_id` int(0) NULL DEFAULT NULL,
  `order_num` int(0) NULL DEFAULT NULL,
  `path` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `component` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `menu_type` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `perms` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` date NULL DEFAULT NULL,
  `update_time` date NULL DEFAULT NULL,
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_menu
-- ----------------------------
INSERT INTO `sys_menu` VALUES (1, '系统管理', 'system', 0, 1, '/sys', '', 'M', '', '2024-07-04', '2024-07-04', '系统管理目录');
INSERT INTO `sys_menu` VALUES (2, '业务管理', 'monitor', 0, 2, '/bsns', '', 'M', '', '2024-07-04', '2024-07-04', '业务管理目录');
INSERT INTO `sys_menu` VALUES (3, '用户管理', 'user', 1, 1, '/sys/user', 'sys/user/index', 'C', 'system:user:list', '2024-07-04', '2024-07-04', '用户管理菜单');
INSERT INTO `sys_menu` VALUES (4, '角色管理', 'peoples', 1, 2, '/sys/role', 'sys/role/index', 'C', 'system:role:list', '2024-07-04', '2024-07-04', '角色管理菜单');
INSERT INTO `sys_menu` VALUES (5, '菜单管理', 'tree-table', 1, 3, '/sys/menu', 'sys/menu/index', 'C', 'system:menu:list', '2024-07-04', '2024-07-04', '菜单管理菜单');
INSERT INTO `sys_menu` VALUES (6, '部门管理', 'tree', 2, 1, '/bsns/department', 'bsns/Department', 'C', '', '2024-07-04', '2024-07-04', '部门管理菜单');
INSERT INTO `sys_menu` VALUES (7, '岗位管理', 'post', 2, 2, '/bsns/post', 'bsns/Post', 'C', '', '2024-07-04', '2024-07-04', '岗位管理菜单');
INSERT INTO `sys_menu` VALUES (8, '数据管理', 'chart', 2, 3, '/bsns/data', 'bsns/Data', 'C', NULL, '2025-02-21', '2025-02-21', '数据管理菜单');
INSERT INTO `sys_menu` VALUES (9, 'AI对话', 'message', 2, 4, '/bsns/ai', 'bsns/Ai', 'C', NULL, '2025-02-21', '2025-02-21', 'ai对话菜单');
INSERT INTO `sys_menu` VALUES (10, '人脸打卡', 'people', 2, 5, '/bsns/face', 'bsns/Face', 'C', NULL, '2025-02-21', '2025-02-21', '人脸打卡菜单');
INSERT INTO `sys_menu` VALUES (11, '人脸录入', 'people', 2, 6, '/bsns/recording', 'bsns/Recording', 'C', NULL, '2025-03-02', '2025-03-02', '人脸录入菜单');

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `code` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `create_time` date NULL DEFAULT NULL,
  `update_time` date NULL DEFAULT NULL,
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO `sys_role` VALUES (1, '超级管理员', 'admin', '2025-01-16', '2024-07-04', '拥有系统最高权限');
INSERT INTO `sys_role` VALUES (2, '普通角色', 'common', '2025-01-16', '2024-07-04', '普通角色');
INSERT INTO `sys_role` VALUES (3, '测试角色', 'test', '2025-01-16', '2024-07-04', '测试角色');
INSERT INTO `sys_role` VALUES (4, '是', NULL, '2025-01-16', '2024-07-04', NULL);
INSERT INTO `sys_role` VALUES (5, '3', NULL, '2025-01-16', '2024-07-04', NULL);
INSERT INTO `sys_role` VALUES (6, '4', NULL, '2025-01-16', '2024-07-04', NULL);
INSERT INTO `sys_role` VALUES (19, '测2', 'cc2', '2025-01-16', '2024-07-04', 'eewew2');
INSERT INTO `sys_role` VALUES (20, 'ccc测试', 'test2', '2025-01-16', '2024-07-04', 'xxx');
INSERT INTO `sys_role` VALUES (21, '今天测试角色', 'todytest', '2025-01-16', '2024-07-04', 'ccc');
INSERT INTO `sys_role` VALUES (22, '12', '123', '2025-01-16', '2024-08-29', '12');

-- ----------------------------
-- Table structure for sys_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_menu`;
CREATE TABLE `sys_role_menu`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `menu_id` int(0) NOT NULL,
  `role_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sys_role_menu_menu_id_5c7ca896_fk_sys_menu_id`(`menu_id`) USING BTREE,
  INDEX `sys_role_menu_role_id_e0dcb43b_fk_sys_role_id`(`role_id`) USING BTREE,
  CONSTRAINT `sys_role_menu_menu_id_5c7ca896_fk_sys_menu_id` FOREIGN KEY (`menu_id`) REFERENCES `sys_menu` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sys_role_menu_role_id_e0dcb43b_fk_sys_role_id` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 139 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role_menu
-- ----------------------------
INSERT INTO `sys_role_menu` VALUES (114, 1, 6);
INSERT INTO `sys_role_menu` VALUES (115, 5, 6);
INSERT INTO `sys_role_menu` VALUES (116, 2, 6);
INSERT INTO `sys_role_menu` VALUES (117, 6, 6);
INSERT INTO `sys_role_menu` VALUES (118, 7, 6);
INSERT INTO `sys_role_menu` VALUES (129, 1, 1);
INSERT INTO `sys_role_menu` VALUES (130, 3, 1);
INSERT INTO `sys_role_menu` VALUES (131, 4, 1);
INSERT INTO `sys_role_menu` VALUES (132, 2, 1);
INSERT INTO `sys_role_menu` VALUES (133, 8, 1);
INSERT INTO `sys_role_menu` VALUES (134, 9, 1);
INSERT INTO `sys_role_menu` VALUES (135, 10, 1);
INSERT INTO `sys_role_menu` VALUES (136, 11, 1);
INSERT INTO `sys_role_menu` VALUES (137, 2, 2);
INSERT INTO `sys_role_menu` VALUES (138, 9, 2);
INSERT INTO `sys_role_menu` VALUES (139, 10, 2);

-- ----------------------------
-- Table structure for sys_security_log
-- ----------------------------
DROP TABLE IF EXISTS `sys_security_log`;
CREATE TABLE `sys_security_log`  (
  `id` bigint(0) NOT NULL AUTO_INCREMENT,
  `event_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `event_data` json NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `user_id` int(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sys_security_log_user_id_7ae49952_fk_sys_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `sys_security_log_user_id_7ae49952_fk_sys_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_security_log
-- ----------------------------
INSERT INTO `sys_security_log` VALUES (1, 'FACE_VERIFY_FAIL', '{}', '2025-03-28 10:41:53.000000', 19);
INSERT INTO `sys_security_log` VALUES (2, 'FACE_VERIFY_FAIL', '{}', '2025-03-28 10:44:25.000000', 20);
INSERT INTO `sys_security_log` VALUES (3, 'FACE_VERIFY_FAIL', '{}', '2025-03-29 04:31:39.443891', 1);
INSERT INTO `sys_security_log` VALUES (4, 'FACE_VERIFY_FAIL', '{}', '2025-04-01 05:07:38.156653', 1);
INSERT INTO `sys_security_log` VALUES (5, 'FACE_VERIFY_FAIL', '{}', '2025-04-07 14:03:57.334927', 1);
INSERT INTO `sys_security_log` VALUES (6, 'LOCATION_MISMATCH', '{}', '2025-04-20 02:54:05.288033', 1);
INSERT INTO `sys_security_log` VALUES (7, 'LOCATION_MISMATCH', '{}', '2025-04-29 03:23:22.025774', 1);
INSERT INTO `sys_security_log` VALUES (8, 'LOCATION_MISMATCH', '{}', '2025-04-29 03:49:16.972989', 1);
INSERT INTO `sys_security_log` VALUES (9, 'LOCATION_MISMATCH', '{}', '2025-04-29 12:01:51.556119', 1);
INSERT INTO `sys_security_log` VALUES (10, 'LOCATION_MISMATCH', '{}', '2025-05-09 16:59:10.596555', 1);
INSERT INTO `sys_security_log` VALUES (11, 'LOCATION_MISMATCH', '{}', '2025-05-09 17:06:24.272947', 1);
INSERT INTO `sys_security_log` VALUES (12, 'LOCATION_MISMATCH', '{}', '2025-05-10 21:54:18.706065', 1);
INSERT INTO `sys_security_log` VALUES (13, 'LOCATION_MISMATCH', '{}', '2025-05-12 21:22:57.721781', 1);
INSERT INTO `sys_security_log` VALUES (14, 'LOCATION_MISMATCH', '{}', '2025-05-12 21:30:06.937592', 1);
INSERT INTO `sys_security_log` VALUES (15, 'LOCATION_MISMATCH', '{}', '2025-05-13 14:46:28.554933', 1);
INSERT INTO `sys_security_log` VALUES (16, 'LOCATION_MISMATCH', '{}', '2025-05-16 16:54:31.063410', 1);
INSERT INTO `sys_security_log` VALUES (17, 'LOCATION_MISMATCH', '{}', '2025-05-25 11:12:00.013800', 1);
INSERT INTO `sys_security_log` VALUES (18, 'LOCATION_MISMATCH', '{}', '2025-05-25 11:12:24.491794', 1);

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `phonenumber` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `login_date` date NULL DEFAULT NULL,
  `status` int(0) NULL DEFAULT NULL,
  `create_time` date NULL DEFAULT NULL,
  `update_time` date NULL DEFAULT NULL,
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES (1, 'zjy', '123456', '20250221175005.jpg', '123@126.com', '18166666666', '2024-08-08', 1, '2025-01-18', '2025-05-10', '超级管理员');
INSERT INTO `sys_user` VALUES (3, '1', '123456', '20240808230603.jpg', 'abc@126.com', '18862857104', '2024-08-08', 0, '2025-01-18', '2025-05-10', '测试用户');
INSERT INTO `sys_user` VALUES (6, '4', '123456', '20240808230603.jpg', NULL, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO `sys_user` VALUES (7, '5', '123456', '20240808230603.jpg', NULL, NULL, NULL, 1, NULL, '2025-04-09', NULL);
INSERT INTO `sys_user` VALUES (8, '6', '123456', '20240808230603.jpg', NULL, NULL, NULL, 0, NULL, NULL, NULL);
INSERT INTO `sys_user` VALUES (11, '9', '123456', '20240808230603.jpg', NULL, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO `sys_user` VALUES (14, '666', '123456', 'default.jpg', 'caofeng2014@126.com', '18862857104', NULL, 1, '2025-01-18', NULL, '33');
INSERT INTO `sys_user` VALUES (15, 'jack', '123456', 'default.jpg', 'caofeng2014@126.com', '18862857104', NULL, 1, '2025-01-18', '2024-09-06', '禁用用户测试4');
INSERT INTO `sys_user` VALUES (16, '12323232', '123456', 'default.jpg', '1@126.com', '18862857104', NULL, 1, '2024-08-18', '2024-08-18', '115');
INSERT INTO `sys_user` VALUES (17, 'marry', '123456', 'default.jpg', '111@qq.com', '15586521012', NULL, 1, '2024-09-05', NULL, '555');
INSERT INTO `sys_user` VALUES (18, 'zhangsan', '123456', '20250327181301.jpg', 'hhh@qq.com', '12345678900', NULL, 1, NULL, NULL, '财务部员工');
INSERT INTO `sys_user` VALUES (19, 'lisi', '123456', '20250327181326.jpg', 'hhh@qq.com', NULL, NULL, 1, NULL, NULL, '市场部员工');
INSERT INTO `sys_user` VALUES (20, 'wangwu', '123456', '20250327181352.jpg', NULL, NULL, NULL, 1, NULL, NULL, '人事部员工');
INSERT INTO `sys_user` VALUES (21, 'zhangsan2', '123456', '20250327181352.jpg', NULL, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO `sys_user` VALUES (22, 'lisi2', '123456', '20250327181352.jpg', NULL, NULL, NULL, 1, NULL, NULL, NULL);
INSERT INTO `sys_user` VALUES (23, 'wangwu2', '123456', '20250327181352.jpg', NULL, NULL, NULL, 1, NULL, NULL, NULL);

-- ----------------------------
-- Table structure for sys_user_department
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_department`;
CREATE TABLE `sys_user_department`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `department_id` bigint(0) NOT NULL,
  `user_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sys_user_department_department_id_24e28309_fk_sys_department_id`(`department_id`) USING BTREE,
  INDEX `sys_user_department_user_id_b07b3269_fk_sys_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `sys_user_department_department_id_24e28309_fk_sys_department_id` FOREIGN KEY (`department_id`) REFERENCES `sys_department` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sys_user_department_user_id_b07b3269_fk_sys_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user_department
-- ----------------------------
INSERT INTO `sys_user_department` VALUES (1, 1, 1);
INSERT INTO `sys_user_department` VALUES (2, 2, 18);
INSERT INTO `sys_user_department` VALUES (3, 3, 19);
INSERT INTO `sys_user_department` VALUES (4, 4, 20);
INSERT INTO `sys_user_department` VALUES (5, 2, 21);
INSERT INTO `sys_user_department` VALUES (6, 3, 22);
INSERT INTO `sys_user_department` VALUES (7, 4, 23);

-- ----------------------------
-- Table structure for sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role`  (
  `id` int(0) NOT NULL AUTO_INCREMENT,
  `role_id` int(0) NOT NULL,
  `user_id` int(0) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `sys_user_role_role_id_63624973_fk_sys_role_id`(`role_id`) USING BTREE,
  INDEX `sys_user_role_user_id_5f2fb964_fk_sys_user_id`(`user_id`) USING BTREE,
  CONSTRAINT `sys_user_role_role_id_63624973_fk_sys_role_id` FOREIGN KEY (`role_id`) REFERENCES `sys_role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `sys_user_role_user_id_5f2fb964_fk_sys_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 52 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user_role
-- ----------------------------
INSERT INTO `sys_user_role` VALUES (1, 1, 1);
INSERT INTO `sys_user_role` VALUES (2, 2, 1);
INSERT INTO `sys_user_role` VALUES (20, 2, 8);
INSERT INTO `sys_user_role` VALUES (21, 20, 8);
INSERT INTO `sys_user_role` VALUES (22, 5, 8);
INSERT INTO `sys_user_role` VALUES (23, 2, 17);
INSERT INTO `sys_user_role` VALUES (27, 2, 15);
INSERT INTO `sys_user_role` VALUES (28, 2, 18);
INSERT INTO `sys_user_role` VALUES (29, 2, 19);
INSERT INTO `sys_user_role` VALUES (30, 2, 20);
INSERT INTO `sys_user_role` VALUES (31, 2, 21);
INSERT INTO `sys_user_role` VALUES (32, 2, 22);
INSERT INTO `sys_user_role` VALUES (33, 2, 23);
INSERT INTO `sys_user_role` VALUES (43, 2, 6);
INSERT INTO `sys_user_role` VALUES (44, 3, 6);
INSERT INTO `sys_user_role` VALUES (45, 5, 6);
INSERT INTO `sys_user_role` VALUES (46, 6, 6);
INSERT INTO `sys_user_role` VALUES (47, 19, 6);
INSERT INTO `sys_user_role` VALUES (48, 20, 6);
INSERT INTO `sys_user_role` VALUES (49, 1, 6);
INSERT INTO `sys_user_role` VALUES (50, 2, 3);
INSERT INTO `sys_user_role` VALUES (51, 3, 3);
INSERT INTO `sys_user_role` VALUES (52, 4, 3);

SET FOREIGN_KEY_CHECKS = 1;
