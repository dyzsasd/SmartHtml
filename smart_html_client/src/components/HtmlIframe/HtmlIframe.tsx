import React, { useEffect, useRef, useState } from "react"

import styles from "./HtmlIframe.module.scss";
import { WebPage } from "../../request/model";

interface HtmlIframeProps { 
    loading: boolean;
    error?: boolean;
    webPage?: WebPage;
    delayLoading?: boolean;
}

const HtmlIframe: React.FC<HtmlIframeProps> = ({loading, webPage, error, delayLoading}) => {

    const [scaleFactor, setScaleFactor] = useState(1);
    const iframeBoxRef = useRef<HTMLDivElement | null>(null)
    
    const [loadingAnimation, setLoadingAnimation] = useState<Boolean>(true)

    /**
        If HTML is not fully rendered, it can lead to incomplete initialization of page animations, 
        resulting in errors such as a scale factor of 0 during calculation. Therefore, 
        we need to implement delayed loading.
     */
    useEffect(() => {
        let timeoutId: NodeJS.Timeout;
    
        if (!loading && delayLoading) {
            timeoutId = setTimeout(() => {
                setLoadingAnimation(loading);
            }, 350);
        } else {
            setLoadingAnimation(loading);
        }
    
        return () => clearTimeout(timeoutId);
    }, [delayLoading, loading]);

    useEffect(() => {
        // Calculate the proportion to prepare for changing the window size in the future
        const calculateScaleFactor = () => {
            if (iframeBoxRef.current){
                const targetWidth = 1920;
                const iframeWidth = iframeBoxRef.current.offsetWidth;
                console.log(iframeWidth)
                const newScaleFactor = iframeWidth / targetWidth;
                setScaleFactor(newScaleFactor);
            }
        };
        
        calculateScaleFactor();

        window.addEventListener('resize', calculateScaleFactor);

        return () => {
            window.removeEventListener('resize', calculateScaleFactor);
        };
    }, [webPage, loadingAnimation]);
    
    const srcDoc = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <style>
                body{
                    // width: ${scaleFactor * 1920}px;
                    // height: ${scaleFactor * 1080}px;
                    transform-origin: top left;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    margin: 0;
                    padding: 0;
                    border: 0;
                    overflow: hidden;
                    transform: scale(${scaleFactor});
                }
                ${webPage?.css}
            </style>
        </head>
        <body>
            ${webPage?.html}
            <script>${webPage?.javascript}</script>
        </body>
        </html>
    `;
                
    return <div className={webPage ? `${styles["html-iframe-box"]}` : `${styles["html-iframe-box"]} ${styles["hidden"]}`}>
        {loadingAnimation ? 
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
