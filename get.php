<?php
$article = article_lookup(intval($_GET['id']));
$json = intval($_GET['json']);
if ( $json == 0 ) echo $article['title'];
else echo '{ "title": "' . addslashes($article['title']) . '" }';


function article_lookup($article_id, $return='title')
{
    // Pull an article, take its pieces. Sometimes we just want the title, sometimes we want more.
    $url = 'http://www.mercurynews.com/portlet/article/html/fragments/print_article.jsp?articleId=' . $article_id . '&amp;siteId=36';
    $content = get_content($url);
    preg_match('/<td class="articleTitle">([^<]+)<\/td>/', $content, $matches);
    $article['title'] = $matches[1];
    if ( $return == 'title' ) return $matches[1];
    // Line-endings in regex's are the tool of the devil.
    $content = str_replace("\n", '', $content);
    $content = str_replace('&', '&amp;', $content);
    preg_match('/<td class="articleBody">(.*)<\/td><\/tr><tr><td>/', $content, $matches);
    if ( count($matches) == 0 ) 
    {
        return false;
    }
    $article['body'] = $matches[1];
    return $article;
}

