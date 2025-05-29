-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-05-2025 a las 04:09:13
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `telefonofinal`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `telefonos`
--
  USE telefonofinal;

CREATE TABLE `telefonos` (
  `id` int(11) NOT NULL,
  `marca` varchar(100) NOT NULL,
  `modelo` varchar(100) NOT NULL,
  `numero_sim` int(11) NOT NULL,
  `imei` int(11) NOT NULL,
  `foto` varchar(5000) NOT NULL,
  `fecha_registro` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `telefonos`
--

INSERT INTO `telefonos` (`id`, `marca`, `modelo`, `numero_sim`, `imei`, `foto`, `fecha_registro`) VALUES
(10, 'Xiaomi', '15 Ultra', 3355677, 32445778, '2025224346xiaomi 15.png', '2025-05-05'),
(11, 'Samsung', 'S25 Ultra', 2147483647, 34345565, '2025103321163x346_Titanium_Silverblue_P3.avif', '2025-02-11'),
(12, 'Xiaomi', 'Note 11', 2147483647, 33445565, '2025103447note 11.jpg', '2025-05-20'),
(13, 'Iphone', '13 PRO', 2147483647, 2147483647, '2025155913images.jpg', '2025-01-15');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `codigo` int(11) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `contraseña` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`codigo`, `correo`, `contraseña`) VALUES
(1, 'carlos@gmail.com', '111');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `telefonos`
--
ALTER TABLE `telefonos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`codigo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `telefonos`
--
ALTER TABLE `telefonos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `codigo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
