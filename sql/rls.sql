-- Row Level Security (RLS) para Tesoros del Barrio
-- Implementa seguridad a nivel de fila para proteger datos de usuarios

-- ============================================
-- POLÍTICAS PARA LA TABLA USUARIOS
-- ============================================

-- Habilitar RLS en la tabla usuarios
ALTER TABLE public.usuarios ENABLE ROW LEVEL SECURITY;

-- Política 1: Los usuarios pueden ver su propio perfil
CREATE POLICY "Usuarios pueden ver su propio perfil"
  ON public.usuarios FOR SELECT
  USING (auth.uid() = id);

-- Política 2: Los usuarios pueden ver perfiles públicos (para mostrar autor en lugares)
CREATE POLICY "Usuarios pueden ver nombres de otros usuarios"
  ON public.usuarios FOR SELECT
  USING (true);  -- Todos pueden ver nombre y email (información pública)

-- Política 3: Los usuarios pueden actualizar solo su propio perfil
CREATE POLICY "Usuarios pueden actualizar su propio perfil"
  ON public.usuarios FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id);

-- Política 4: Los usuarios pueden insertar su propio registro
CREATE POLICY "Usuarios pueden crear su propio perfil"
  ON public.usuarios FOR INSERT
  WITH CHECK (auth.uid() = id);

-- Política 5: Los usuarios pueden eliminar su propio registro
CREATE POLICY "Usuarios pueden eliminar su propio perfil"
  ON public.usuarios FOR DELETE
  USING (auth.uid() = id);

-- ============================================
-- POLÍTICAS PARA LA TABLA LUGARES
-- ============================================

-- Habilitar RLS en la tabla lugares
ALTER TABLE public.lugares ENABLE ROW LEVEL SECURITY;

-- Política 1: Todos pueden VER todos los lugares
CREATE POLICY "Todos pueden ver todos los lugares"
  ON public.lugares FOR SELECT
  USING (true);

-- Política 2: Los usuarios autenticados pueden CREAR nuevos lugares
CREATE POLICY "Usuarios autenticados pueden crear lugares"
  ON public.lugares FOR INSERT
  WITH CHECK (
    auth.role() = 'authenticated'
    AND autor_id = auth.uid()
  );

-- Política 3: Los usuarios pueden EDITAR solo sus propios lugares
CREATE POLICY "Usuarios pueden editar solo sus propios lugares"
  ON public.lugares FOR UPDATE
  USING (auth.uid() = autor_id)
  WITH CHECK (
    auth.uid() = autor_id
  );

-- Política 4: Los usuarios pueden ELIMINAR solo sus propios lugares
CREATE POLICY "Usuarios pueden eliminar solo sus propios lugares"
  ON public.lugares FOR DELETE
  USING (auth.uid() = autor_id);

-- ============================================
-- POLÍTICAS PARA LA TABLA LOGS_ACTIVIDAD
-- ============================================

-- Habilitar RLS en la tabla logs_actividad
ALTER TABLE public.logs_actividad ENABLE ROW LEVEL SECURITY;

-- Política 1: Los usuarios solo pueden ver sus propios logs
CREATE POLICY "Usuarios pueden ver sus propios logs"
  ON public.logs_actividad FOR SELECT
  USING (auth.uid() = usuario_id OR usuario_id IS NULL);

-- Política 2: La aplicación puede insertar logs (sin restricción)
CREATE POLICY "Aplicación puede insertar logs"
  ON public.logs_actividad FOR INSERT
  WITH CHECK (true);

-- ============================================
-- FUNCIONES DE SEGURIDAD ADICIONALES
-- ============================================

-- Función para obtener el ID del usuario autenticado
CREATE OR REPLACE FUNCTION public.get_usuario_id()
RETURNS UUID AS $$
  SELECT auth.uid();
$$ LANGUAGE SQL SECURITY DEFINER;

-- Función para verificar si el usuario es propietario de un lugar
CREATE OR REPLACE FUNCTION public.es_propietario_lugar(lugar_id UUID)
RETURNS BOOLEAN AS $$
  SELECT EXISTS(
    SELECT 1 FROM public.lugares
    WHERE id = lugar_id AND autor_id = auth.uid()
  );
$$ LANGUAGE SQL SECURITY DEFINER;

-- Comentarios de documentación
COMMENT ON POLICY "Todos pueden ver todos los lugares" ON public.lugares IS 'Política de lectura pública: todos ven todos los lugares';
COMMENT ON POLICY "Usuarios pueden editar solo sus propios lugares" ON public.lugares IS 'Política de actualización: solo el autor puede editar';
COMMENT ON POLICY "Usuarios pueden eliminar solo sus propios lugares" ON public.lugares IS 'Política de eliminación: solo el autor puede eliminar';
