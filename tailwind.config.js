/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: "class",
  content: ["./*.html", "./hizmetler/**/*.html"],
  theme: {
    extend: {
      colors: {
        "surface-bright": "#393939",
        "on-secondary-fixed-variant": "#5b4300",
        "on-primary-fixed": "#410002",
        primary: "#e53935",
        "outline-variant": "#5b403d",
        "on-tertiary-fixed": "#1a1c1c",
        "inverse-surface": "#e5e2e1",
        "on-primary": "#ffffff",
        "surface-container-highest": "#353534",
        "on-background": "#e5e2e1",
        "on-tertiary-container": "#282a2a",
        "on-secondary-fixed": "#261a00",
        secondary: "#ffdf9e",
        "on-secondary": "#3f2e00",
        "on-surface": "#e5e2e1",
        "error-container": "#93000a",
        background: "#131313",
        "surface-dim": "#131313",
        "tertiary-fixed": "#e2e2e2",
        "tertiary-container": "#909191",
        "surface-container-low": "#1c1b1b",
        surface: "#131313",
        "secondary-container": "#fabd00",
        outline: "#ab8985",
        "primary-container": "#b71c1c",
        "on-tertiary-fixed-variant": "#454747",
        "inverse-on-surface": "#313030",
        "surface-container-high": "#2a2a2a",
        "primary-fixed": "#ffcdd2",
        error: "#ffb4ab",
        "primary-fixed-dim": "#e53935",
        "on-error-container": "#ffcdd2",
        "on-surface-variant": "#e4beb9",
        "surface-container": "#201f1f",
        "on-error": "#690005",
        "surface-tint": "#e53935",
        "secondary-fixed": "#ffdf9e",
        "surface-variant": "#353534",
        tertiary: "#c6c6c7",
        "on-secondary-container": "#6a4e00",
        "secondary-fixed-dim": "#fabd00",
        "on-tertiary": "#2f3131",
        "surface-container-lowest": "#0e0e0e",
        "on-primary-fixed-variant": "#93000d",
        "on-primary-container": "#ffffff",
        "tertiary-fixed-dim": "#c6c6c7",
        "inverse-primary": "#bb171c"
      },
      borderRadius: {
        DEFAULT: "0.125rem",
        lg: "0.25rem",
        xl: "0.5rem",
        full: "0.75rem"
      },
      spacing: {
        "margin-mobile": "16px",
        gutter: "24px",
        base: "8px",
        "section-gap": "80px",
        "margin-desktop": "64px"
      },
      fontFamily: {
        "body-lg": ["Roboto Flex"],
        "display-lg": ["Oswald"],
        "label-bold": ["Oswald"],
        "headline-lg": ["Oswald"],
        "title-md": ["Oswald"],
        "headline-lg-mobile": ["Oswald"],
        "body-md": ["Roboto Flex"]
      },
      fontSize: {
        "body-lg": ["18px", { lineHeight: "28px", fontWeight: "400" }],
        "display-lg": ["48px", { lineHeight: "56px", fontWeight: "700" }],
        "label-bold": ["14px", { lineHeight: "20px", letterSpacing: "0.1em", fontWeight: "600" }],
        "headline-lg": ["32px", { lineHeight: "40px", fontWeight: "600" }],
        "title-md": ["20px", { lineHeight: "28px", letterSpacing: "0.05em", fontWeight: "500" }],
        "headline-lg-mobile": ["28px", { lineHeight: "36px", fontWeight: "600" }],
        "body-md": ["16px", { lineHeight: "24px", fontWeight: "400" }]
      },
      animation: {
        "fade-in-up": "fade-in-up 0.6s ease-out forwards",
        "fade-in-up-delay-1": "fade-in-up 0.6s ease-out 0.2s forwards",
        "fade-in-up-delay-2": "fade-in-up 0.6s ease-out 0.4s forwards",
        float: "float 6s ease-in-out infinite",
        "pulse-slow": "pulseSlow 3s infinite",
        beam: "beam 10s linear infinite",
        shimmer: "shimmer 3s infinite linear"
      },
      keyframes: {
        fadeInUp: {
          "0%": { opacity: "0", transform: "translateY(30px)" },
          "100%": { opacity: "1", transform: "translateY(0)" }
        },
        "fade-in-up": {
          "0%": { opacity: "0", transform: "translateY(20px)" },
          "100%": { opacity: "1", transform: "translateY(0)" }
        },
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-15px)" }
        },
        pulseSlow: {
          "0%, 100%": { transform: "scale(1)", boxShadow: "0 0 0 0 rgba(250,189,0,0.4)" },
          "50%": { transform: "scale(1.05)", boxShadow: "0 0 20px 5px rgba(250,189,0,0.2)" }
        },
        beam: {
          "0%": { transform: "translateX(-100%) rotate(-45deg)" },
          "100%": { transform: "translateX(200%) rotate(-45deg)" }
        },
        shimmer: {
          "0%": { backgroundPosition: "200% 0" },
          "100%": { backgroundPosition: "-200% 0" }
        }
      }
    }
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/container-queries")
  ]
};
