import * as yup from 'yup'

// Validation schema
export const schema = yup.object({
  titel: yup.string().required('Angabe ist erforderlich'),
  slug: yup
    .string()
    .required('Angabe ist erforderlich')
    .matches(/^[a-z0-9]+(-[a-z0-9]+)*$/, 'Nur Kleinbuchstaben, Ziffern und Bindestriche erlaubt'),
  inhalt: yup.string().nullable(),
  zeigtKontaktButton: yup.boolean().default(false)
})
