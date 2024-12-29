import * as React from "react";
import { CSSProperties, DetailedHTMLProps, HTMLAttributes } from "react";

interface LengthObject {
    value: number;
    unit: string;
  }
  
  const cssUnit: { [unit: string]: boolean } = {
    cm: true,
    mm: true,
    in: true,
    px: true,
    pt: true,
    pc: true,
    em: true,
    ex: true,
    ch: true,
    rem: true,
    vw: true,
    vh: true,
    vmin: true,
    vmax: true,
    "%": true,
};

function parseLengthAndUnit(size: number | string): LengthObject {
    if (typeof size === "number") {
      return {
        value: size,
        unit: "px",
      };
    }
    let value: number;
    const valueString: string = (size.match(/^[0-9.]*/) || "").toString();
    if (valueString.includes(".")) {
      value = parseFloat(valueString);
    } else {
      value = parseInt(valueString, 10);
    }
  
    const unit: string = (size.match(/[^0-9]*$/) || "").toString();
  
    if (cssUnit[unit]) {
      return {
        value,
        unit,
      };
    }
  
    console.warn(`React Spinners: ${size} is not a valid css value. Defaulting to ${value}px.`);
  
    return {
      value,
      unit: "px",
    };
  }

export function cssValue(value: number | string): string {
    const lengthWithunit = parseLengthAndUnit(value);
  
    return `${lengthWithunit.value}${lengthWithunit.unit}`;
}

type LengthType = number | string;

interface CommonProps extends DetailedHTMLProps<HTMLAttributes<HTMLSpanElement>, HTMLSpanElement> {
  color?: string;
  loading?: boolean;
  cssOverride?: CSSProperties;
  speedMultiplier?: number;
}

export interface LoaderHeightWidthProps extends CommonProps {
  height?: LengthType;
  width?: LengthType;
}

export interface LoaderSizeProps extends CommonProps {
  size?: LengthType;
}

export interface LoaderSizeMarginProps extends CommonProps {
  size?: LengthType;
  margin?: LengthType;
}

export interface LoaderHeightWidthRadiusProps extends CommonProps {
  height?: LengthType;
  width?: LengthType;
  radius?: LengthType;
  margin?: LengthType;
}

export const createAnimation = (loaderName: string, frames: string, suffix: string): string => {
    const animationName = `react-spinners-${loaderName}-${suffix}`;
  
    if (typeof window == "undefined" || !window.document) {
      return animationName;
    }
  
    const styleEl = document.createElement("style");
    document.head.appendChild(styleEl);
    const styleSheet = styleEl.sheet;
  
    const keyFrames = `
      @keyframes ${animationName} {
        ${frames}
      }
    `;
  
    if (styleSheet) {
      styleSheet.insertRule(keyFrames, 0);
    }
  
    return animationName;
};

const scale = createAnimation(
  "ScaleLoader",
  "0% {transform: scaley(1.0)} 50% {transform: scaley(0.4)} 100% {transform: scaley(1.0)}",
  "scale"
);

function Loader({
  loading = true,
  color = "#000000",
  speedMultiplier = 0.75,
  cssOverride = {},
  height = 24,
  width = 4,
  radius = 2,
  margin = 2,
  ...additionalprops
}: LoaderHeightWidthRadiusProps): JSX.Element | null {
  const wrapper: React.CSSProperties = {
    display: "inherit",
    ...cssOverride,
  };

  const style = (i: number): React.CSSProperties => {
    return {
      backgroundColor: color,
      width: cssValue(width),
      height: cssValue(height),
      margin: cssValue(margin),
      borderRadius: cssValue(radius),
      display: "inline-block",
      animation: `${scale} ${1 / speedMultiplier}s ${i * 0.1}s infinite cubic-bezier(0.2, 0.68, 0.18, 1.08)`,
      animationFillMode: "both",
    };
  };

  if (!loading) {
    return null;
  }

  return (
    <span style={wrapper} {...additionalprops}>
      <span style={style(1)} />
      <span style={style(2)} />
      <span style={style(3)} />
    </span>
  );
}

export default Loader;