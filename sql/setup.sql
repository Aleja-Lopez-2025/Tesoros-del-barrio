-- Tabla de Usuarios
-- Nota: Supabase crea automáticamente la tabla auth.users
-- Esta tabla almacena información adicional de perfil

CREATE TABLE public.usuarios (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  nombre VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  foto_perfil_url TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Lugares (Lugares interesantes del barrio)
CREATE TABLE public.lugares (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  nombre VARCHAR(150) NOT NULL,
  descripcion TEXT NOT NULL,
  categoria VARCHAR(50) NOT NULL CHECK (
    categoria IN ('Parque', 'Heladería', 'Mural', 'Mascotas', 'Lugar secreto', 'Otro')
  ),
  latitud DECIMAL(10, 8) NOT NULL,
  longitud DECIMAL(11, 8) NOT NULL,
  foto_url TEXT,
  autor_id UUID NOT NULL REFERENCES public.usuarios(id) ON DELETE CASCADE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
  -- Índices para mejorar rendimiento
  CONSTRAINT coords_check CHECK (
    latitud >= -90 AND latitud <= 90 AND 
    longitud >= -180 AND longitud <= 180
  )
);

-- Índices para búsquedas geoespaciales y consultas frecuentes
CREATE INDEX idx_lugares_autor_id ON public.lugares(autor_id);
CREATE INDEX idx_lugares_categoria ON public.lugares(categoria);
CREATE INDEX idx_lugares_created_at ON public.lugares(created_at DESC);
CREATE INDEX idx_lugares_coords ON public.lugares(latitud, longitud);

-- Tabla para auditoría y estadísticas (opcional)
CREATE TABLE public.logs_actividad (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  usuario_id UUID REFERENCES public.usuarios(id) ON DELETE SET NULL,
  tipo_accion VARCHAR(50) NOT NULL,
  descripcion TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_logs_usuario_id ON public.logs_actividad(usuario_id);
CREATE INDEX idx_logs_created_at ON public.logs_actividad(created_at DESC);

-- Trigger para actualizar updated_at en usuarios
CREATE OR REPLACE FUNCTION public.update_updated_at_usuarios()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_updated_at_usuarios
BEFORE UPDATE ON public.usuarios
FOR EACH ROW
EXECUTE FUNCTION public.update_updated_at_usuarios();

-- Trigger para actualizar updated_at en lugares
CREATE OR REPLACE FUNCTION public.update_updated_at_lugares()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = CURRENT_TIMESTAMP;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_updated_at_lugares
BEFORE UPDATE ON public.lugares
FOR EACH ROW
EXECUTE FUNCTION public.update_updated_at_lugares();

-- Comentarios de documentación
COMMENT ON TABLE public.usuarios IS 'Tabla de perfiles de usuarios. Información adicional más allá de auth.users';
COMMENT ON TABLE public.lugares IS 'Tabla de lugares interesantes compartidos por usuarios en el barrio';
COMMENT ON COLUMN public.lugares.categoria IS 'Categoría del lugar: Parque, Heladería, Mural, Mascotas, Lugar secreto, Otro';
COMMENT ON COLUMN public.lugares.latitud IS 'Latitud en formato decimal (-90 a 90)';
COMMENT ON COLUMN public.lugares.longitud IS 'Longitud en formato decimal (-180 a 180)';
