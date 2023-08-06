//
// Copyright (C) 2018 by the adcc authors
//
// This file is part of adcc.
//
// adcc is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published
// by the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// adcc is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with adcc. If not, see <http://www.gnu.org/licenses/>.
//

#pragma once
#include <memory>

namespace adcc {
/**
 *  \addtogroup Utilities
 */
///@{

/** Pool managing how many threads may be used for calculations. */
class ThreadPool {
 public:
  /** Initialise the thread pool.
   *
   * \param  n_cores    The number of cpu cores to employ
   * \param  n_threads  The number of threads to use
   *                    (default 2*n_cores - 1)
   */
  ThreadPool(size_t n_cores, size_t n_threads) : m_holder_ptr{nullptr} {
    reinit(n_cores, n_threads);
  }

  /** Reinitialise the thread pool.
   *
   * \param  n_cores    The number of cpu cores to employ
   * \param  n_threads  The number of threads to use
   */
  void reinit(size_t n_cores, size_t n_threads);

  /** Initialise a thread pool without parallelisation */
  ThreadPool() : ThreadPool(1, 1) {}

  /** Return the number of cores employed for parallelisation. */
  size_t n_cores() const { return m_n_cores; }

  /** Return the number of threads employed for parallelisation. */
  size_t n_threads() const { return m_n_threads; }

  // Avoid copying or copy-assinging
  ThreadPool(const ThreadPool&) = delete;
  ThreadPool& operator=(const ThreadPool&) = delete;

  ~ThreadPool();

 private:
  // Hack to avoid the libutil data structures in the interface
  std::shared_ptr<void> m_holder_ptr;
  size_t m_n_cores;
  size_t m_n_threads;
};

///@}
}  // namespace adcc
