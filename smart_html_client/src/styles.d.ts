declare module '*.module.scss' {
  const classes: { [key: string]: string };
  export default classes;
}
declare interface ImportMetaEnv {
  MODE: string;
}
