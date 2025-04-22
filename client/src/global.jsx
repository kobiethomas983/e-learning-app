export const ShowIf = ({ condition, children }) => {
    return condition ? <>{children}</> : null;
  };