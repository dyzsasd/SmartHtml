import React, { useState } from "react"

import styles from "./HtmlIframe.module.scss";

interface HtmlIframeProps { 
    view: boolean;
}

const HtmlIframe: React.FC<HtmlIframeProps> = ({view}) => {

    return <div className={view ? `${styles["html-iframe-box"]}` : `${styles["html-iframe-box"]} ${styles["hidden"]}`}>
       
    </div>
}

export default HtmlIframe;
