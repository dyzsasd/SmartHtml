import React, { useEffect, useRef, useState } from "react"

import styles from "./HtmlIframe.module.scss";

interface HtmlIframeProps { 
    view: boolean;
    loading: boolean;
    error?: boolean;
    html?: string;
    css?: string;
    js?: string;
}

const HtmlIframe: React.FC<HtmlIframeProps> = ({view, loading, html, css, js, error}) => {

    const [scaleFactor, setScaleFactor] = useState(1);

    const iframeBoxRef = useRef<HTMLDivElement | null>(null)

    useEffect(() => {
        // Calculate the proportion to prepare for changing the window size in the future
        const calculateScaleFactor = () => {
            if (iframeBoxRef.current){
                const targetWidth = 1920;
                const iframeWidth = iframeBoxRef.current.offsetWidth;
                const newScaleFactor = iframeWidth / targetWidth;
                setScaleFactor(newScaleFactor);
            }
        };

        calculateScaleFactor();
        window.addEventListener('resize', calculateScaleFactor);

        return () => {
            window.removeEventListener('resize', calculateScaleFactor);
        };
    }, [html, css, js, loading]);
    
    const srcDoc = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <style>
                body{
                    width: ${scaleFactor * 1920}px;
                    height: ${scaleFactor * 1080}px;
                    transform-origin: top left;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin: 0;
                    padding: 0;
                    border: 0;
                    overflow: hidden;
                }
                ${css}
            </style>
        </head>
        <body>
            ${html}
            <script>${js}</script>
        </body>
        </html>
    `;
                
    return <div className={view ? `${styles["html-iframe-box"]}` : `${styles["html-iframe-box"]} ${styles["hidden"]}`}>
        {loading ? 
            <div className={styles["loading-box"]}>
                <div className={`${styles["loading-animation"]} ${error ? styles["loading-animation-error"] : ""}`}></div>
            </div> : 
            <div className={styles["iframe-box"]} ref={iframeBoxRef}>
                <iframe 
                    srcDoc={srcDoc}
                    title="Smart html"
                />
            </div>
        }
    </div>
}

export default HtmlIframe;
