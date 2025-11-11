import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PharmacySearch.css';

const PharmacySearch = () => {
  const [keyword, setKeyword] = useState('');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({
    currentPage: 1,
    maxResultCount: 16,
    totalCount: 0
  });
  const [sortType, setSortType] = useState(4);
  const [aggregations, setAggregations] = useState([]);

  const searchProducts = async (skipCount = 0) => {
    if (!keyword.trim()) {
      setProducts([]);
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await axios.post(
        'https://api.nhathuoclongchau.com.vn/lccus/search-product-service/api/products/ecom/product/search',
        {
          keyword: keyword,
          maxResultCount: pagination.maxResultCount,
          skipCount: skipCount,
          sortType: sortType,
          codes: [
            "category",
            "objectUse",
            "indications",
            "prescription",
            "skin",
            "flavor",
            "manufactor",
            "brand",
            "brandOrigin"
          ],
          suggestSize: 6
        },
        {
          headers: {
            'Content-Type': 'application/json'
          }
        }
      );

      // API trả về với structure: { products: [...], totalCount: ..., aggregations: [...] }
      const productsData = response.data.products || response.data.items || [];
      const total = response.data.totalCount || response.data.total || 0;
      const aggs = response.data.aggregations || [];
      
      setProducts(productsData);
      setAggregations(aggs);
      setPagination(prev => ({
        ...prev,
        totalCount: total
      }));
    } catch (err) {
      setError('Không thể tải dữ liệu sản phẩm. Vui lòng thử lại.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (e) => {
    e.preventDefault();
    setPagination(prev => ({ ...prev, currentPage: 1 }));
    searchProducts(0);
  };

  const handlePageChange = (newPage) => {
    const skipCount = (newPage - 1) * pagination.maxResultCount;
    setPagination(prev => ({ ...prev, currentPage: newPage }));
    searchProducts(skipCount);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const totalPages = Math.ceil(pagination.totalCount / pagination.maxResultCount);

  const formatPrice = (price) => {
    if (!price || price === null) return null;
    return new Intl.NumberFormat('vi-VN', {
      style: 'currency',
      currency: 'VND'
    }).format(price);
  };

  const getPriceDisplay = (product) => {
    // Trường hợp 1: price.price có giá trị
    if (product.price?.price) {
      return {
        value: formatPrice(product.price.price),
        unit: product.price.measureUnitName
      };
    }
    
    // Trường hợp 2: price.price là null, tìm trong mảng prices
    if (product.prices && Array.isArray(product.prices)) {
      const priceWithValue = product.prices.find(p => p.price !== null && p.price > 0);
      if (priceWithValue) {
        return {
          value: formatPrice(priceWithValue.price),
          unit: priceWithValue.measureUnitName
        };
      }
    }
    
    // Trường hợp 3: Không có giá
    return { value: null, unit: null };
  };

  return (
    <div className="pharmacy-search-container">
      <div className="search-header">
        <h2>Tìm kiếm thuốc</h2>
        <form onSubmit={handleSearch} className="search-form">
          <div className="search-input-group">
            <input
              type="text"
              placeholder="Nhập tên thuốc cần tìm..."
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              className="search-input"
            />
            <button type="submit" className="search-button" disabled={loading}>
              {loading ? 'Đang tìm...' : 'Tìm kiếm'}
            </button>
          </div>
          
          <div className="filter-group">
            <label>Sắp xếp:</label>
            <select 
              value={sortType} 
              onChange={(e) => setSortType(Number(e.target.value))}
              className="sort-select"
            >
              <option value={1}>Mới nhất</option>
              <option value={2}>Giá thấp đến cao</option>
              <option value={3}>Giá cao đến thấp</option>
              <option value={4}>Phổ biến nhất</option>
            </select>
          </div>
        </form>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      {loading && (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Đang tải dữ liệu...</p>
        </div>
      )}

      {!loading && products.length > 0 && (
        <>
          <div className="results-info">
            Tìm thấy <strong>{pagination.totalCount}</strong> sản phẩm
          </div>

          <div className="products-grid">
            {products.map((product, index) => {
              const priceInfo = getPriceDisplay(product);
              
              return (
                <div key={product.sku || product.id || index} className="product-card">
                  <div className="product-image">
                    <img 
                      src={product.image || '/placeholder.png'} 
                      alt={product.webName || product.name}
                      onError={(e) => {
                        e.target.src = '/placeholder.png';
                      }}
                    />
                    {product.displayCode === 2 && (
                      <span className="prescription-badge">Kê đơn</span>
                    )}
                    {product.sku && (
                      <span className="sku-badge">SKU: {product.sku}</span>
                    )}
                  </div>
                  
                  <div className="product-info">
                    <h3 className="product-name" title={product.webName || product.name}>
                      {product.webName || product.name}
                    </h3>
                    
                    {product.ingredients && (
                      <p className="product-ingredients">
                        <strong>Thành phần:</strong> {product.ingredients.length > 80 
                          ? product.ingredients.substring(0, 80) + '...' 
                          : product.ingredients}
                      </p>
                    )}
                    
                    {product.dosageForm && (
                      <p className="product-dosage">
                        <strong>Dạng:</strong> {product.dosageForm}
                      </p>
                    )}
                    
                    {product.brand && (
                      <p className="product-brand">
                        <strong>Thương hiệu:</strong> {product.brand}
                      </p>
                    )}
                    
                    {product.specification && (
                      <p className="product-spec">
                        <strong>Quy cách:</strong> {product.specification}
                      </p>
                    )}
                    
                    <div className="product-price">
                      {priceInfo.value ? (
                        <>
                          <span className="current-price">
                            {priceInfo.value}
                          </span>
                          {priceInfo.unit && (
                            <span className="measure-unit">
                              / {priceInfo.unit}
                            </span>
                          )}
                        </>
                      ) : (
                        <span className="contact-price">Liên hệ để biết giá</span>
                      )}
                    </div>
                    
                    {product.category && product.category.length > 0 && (
                      <div className="product-categories">
                        {product.category.slice(0, 2).map((cat, idx) => (
                          <span key={idx} className="category-tag" title={cat.slug}>
                            {cat.name}
                          </span>
                        ))}
                      </div>
                    )}
                    
                    <a 
                      href={`https://nhathuoclongchau.com.vn/${product.slug}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="view-detail-button"
                    >
                      Xem chi tiết →
                    </a>
                  </div>
                </div>
              );
            })}
          </div>

          {totalPages > 1 && (
            <div className="pagination">
              <button
                onClick={() => handlePageChange(pagination.currentPage - 1)}
                disabled={pagination.currentPage === 1}
                className="pagination-button"
              >
                ← Trước
              </button>
              
              <div className="pagination-info">
                Trang {pagination.currentPage} / {totalPages}
              </div>
              
              <button
                onClick={() => handlePageChange(pagination.currentPage + 1)}
                disabled={pagination.currentPage >= totalPages}
                className="pagination-button"
              >
                Sau →
              </button>
            </div>
          )}
        </>
      )}

      {!loading && products.length === 0 && keyword && (
        <div className="no-results">
          <p>Không tìm thấy sản phẩm nào phù hợp với từ khóa "<strong>{keyword}</strong>"</p>
        </div>
      )}

      {aggregations.length > 0 && products.length > 0 && (
        <div className="aggregations-section">
          <h3>Bộ lọc có sẵn</h3>
          <div className="aggregations-grid">
            {aggregations.map((agg, idx) => (
              agg.values && agg.values.length > 0 && (
                <div key={idx} className="aggregation-item">
                  <h4>{agg.code === 'category' ? 'Danh mục' :
                      agg.code === 'brand' ? 'Thương hiệu' :
                      agg.code === 'manufactor' ? 'Nhà sản xuất' :
                      agg.code === 'brandOrigin' ? 'Xuất xứ' :
                      agg.code === 'objectUse' ? 'Đối tượng sử dụng' :
                      agg.code === 'indications' ? 'Chỉ định' :
                      agg.code === 'prescription' ? 'Kê đơn' :
                      agg.code}</h4>
                  <div className="aggregation-values">
                    {agg.values.slice(0, 10).map((value, vIdx) => (
                      <span key={vIdx} className="agg-value">
                        {value === 'true' ? 'Có kê đơn' : 
                         value === 'false' ? 'Không kê đơn' : 
                         value || '(Trống)'}
                      </span>
                    ))}
                    {agg.values.length > 10 && (
                      <span className="agg-more">+{agg.values.length - 10} thêm</span>
                    )}
                  </div>
                </div>
              )
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PharmacySearch;
