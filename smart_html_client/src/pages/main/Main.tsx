import React, { useState } from "react";

import PromptInput from "../../components/PromptInput"
import HtmlIframe from "../../components/HtmlIframe"
import styles from './Main.module.scss';


const Main: React.FC = () => {

    const [viewHtml, setViewHtml] = useState<boolean>(false)

    const sendPrompt = () => {
        setViewHtml(true)
    }

    return <div className={styles.main}>
        <HtmlIframe view={viewHtml}/>
        <div className={viewHtml ? `${styles['input-title-hidden']} ${styles['input-title']}` : styles['input-title']}>Let's create your dream web page</div>
        <PromptInput handleEnterDown={sendPrompt}/>
    </div>
}

export default Main;
